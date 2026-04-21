import gradio as gr
import subprocess
import tempfile
import os

def run_riscv(code: str) -> str:
    current_dir = os.getcwd()
    source_dir = os.path.join(current_dir, "src")
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".s")
    relative_path = os.path.relpath(source_dir, os.path.dirname(temp_file.name))
    
    code = code.replace("SOURCE_DIR", relative_path)
    
    temp_file.write(code.encode())
    temp_file.close()
    
    process = subprocess.Popen(
        ["java", "-jar", "venus-61c.dev.jar", temp_file.name],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    ) 
    stdout, stderr = process.communicate()
    return stdout, stderr

# if you want, you can add verification logic via python (one-liner for each function)

def extract_iban(iban: str, verify: bool) -> str:
    code = f"""
	.data
ibanstr:
	.asciiz "{iban}"
knrbuf:
	.space 10
	.asciiz ""
blzbuf:
	.space 8
	.asciiz ""
	.text
	.import "SOURCE_DIR/util.s"
	.import "SOURCE_DIR/iban2knr.s"
 """+(
     """
	.import "SOURCE_DIR/moduloStr.s"
	.import "SOURCE_DIR/validateChecksum.s"
     """ if verify else ""
 )+"""
	.globl main
main:
	la	a0 ibanstr
	la	a1 blzbuf
	la	a2 knrbuf
	jal	iban2knr
	la	a0 blzbuf
	li	a1 8
	jal	println_range
	la	a0 knrbuf
	li	a1 10
	jal	println_range
 """+(
    """
	la	a0 ibanstr
	jal	validate_checksum
	mv	a1 a0
	li	a0 1
	ecall
    """ if verify else ""
 )+"""
	li	a0 10 # exit
	ecall
    """
    try:
        stdout, stderr = run_riscv(code)
        if stderr:
            return f"Error: {stderr}"
        outputs = stdout.strip().splitlines()
        if len(outputs) < 2:
            return "Error: Unexpected output format, got output:\n" + stdout
        blz = outputs[0].strip()
        knr = outputs[1].strip()
        output = f"BLZ: {blz}, KNR: {knr}"
        if verify:
            checksum = outputs[2].strip()
            output += " (Checksum valid)" if checksum == "1" else f" (Checksum invalid, got {checksum})"
        return output
    except Exception as e:
        return f"Exception occurred: {str(e)}"

def generate_iban(blz: str, knr: str) -> str:
    code = f"""
        .data
testblz:
	.asciiz "{blz}"
testknr:
	.asciiz "{knr}"
ibanbuf:
	.space 23
        .text
        .import "SOURCE_DIR/util.s"
        .import "SOURCE_DIR/moduloStr.s"
        .import "SOURCE_DIR/validateChecksum.s"
        .import "SOURCE_DIR/knr2iban.s"
        .globl main
    main:
        la	a0 ibanbuf
        la	a1 testblz
        la	a2 testknr
        jal	knr2iban
        la	a0 ibanbuf
        li	a1 22
        jal	println_range
        ecall
        li	a0 10
        ecall
    """
    try:
        stdout, stderr = run_riscv(code)
        if stderr:
            return f"Error: {stderr}"
        return stdout.strip()
    except Exception as e:
        return f"Exception occurred: {str(e)}"

def calculate_modulo(large_num: str, divisor: str) -> str:
    code = f"""
        .data
    numberstr:
        .asciiz "{large_num}"
        .text
        .import "SOURCE_DIR/util.s"
        .import "SOURCE_DIR/moduloStr.s"
        .globl main
    main:
        la	a0 numberstr
        li	a1 {len(large_num)}
        li	a2 {int(divisor)}
        jal	modulo_str
        mv	a1 a0
        li	a0 1 # print result
        ecall
        li	a0 10 # exit
        ecall
    """
    try:
        stdout, stderr = run_riscv(code)
        if stderr:
            return f"Error: {stderr}"
        return stdout.strip()
    except Exception as e:
        return f"Exception occurred: {str(e)}"


with gr.Blocks(title="IBAN") as demo:
    gr.Markdown("# IBAN")
    
    with gr.Tab("Extract IBAN"):
        gr.Markdown("Extract BLZ and KNR from a German IBAN.")
        with gr.Row():
            iban_input = gr.Textbox(label="German IBAN")
            verify_check = gr.Checkbox(label="Verify Checksum")
        extract_btn = gr.Button("Extract Details")
        extract_output = gr.Textbox(label="Result", interactive=False)
        
        extract_btn.click(
            fn=extract_iban, 
            inputs=[iban_input, verify_check], 
            outputs=extract_output
        )

    with gr.Tab("Generate IBAN"):
        gr.Markdown("Generate a German IBAN from BLZ and Kontonummer.")
        with gr.Row():
            blz_input = gr.Textbox(label="BLZ (8 digits)")
            knr_input = gr.Textbox(label="Kontonummer (up to 10 digits)")
        generate_btn = gr.Button("Generate IBAN")
        generate_output = gr.Textbox(label="Result", interactive=False)
        
        generate_btn.click(
            fn=generate_iban, 
            inputs=[blz_input, knr_input], 
            outputs=generate_output
        )

    with gr.Tab("Large Modulo"):
        gr.Markdown("Calculate modulo for arbitrarily large numbers.")
        large_num_input = gr.Textbox(label="Large Number")
        divisor_input = gr.Textbox(label="Divisor (up to 32-bit int)")
        modulo_btn = gr.Button("Calculate Modulo")
        modulo_output = gr.Textbox(label="Result", interactive=False)
        
        modulo_btn.click(
            fn=calculate_modulo, 
            inputs=[large_num_input, divisor_input], 
            outputs=modulo_output
        )

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=8082)