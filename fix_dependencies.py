import subprocess
import sys

def run_command(command):
    print(f"Running: {command}")
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print(f"Errors: {result.stderr}")
    return result.returncode

def main():
    print("Fixing OpenAI and httpx compatibility issue...")
    
    # Uninstall current versions
    run_command("pip uninstall -y openai httpx")
    
    # Install specific versions
    run_command("pip install httpx==0.27.2")
    run_command("pip install openai==1.55.3")
    
    print("\nDependencies fixed! You can now run the brochure generator.")
    print("Try running: python brochure_generator.py")

if __name__ == "__main__":
    main() 