from fastmcp import FastMCP
import subprocess


mcp = FastMCP(name="MyFirstMCPServer")

@mcp.tool
def greet(name:str) -> str:
    """Returns a friendly greeting"""
    return f"Hello {name}! Its a pleasure to connect from your first MCP Server."

@mcp.tool
def validate_json_with_yaml_schema(json_file_path: str, yaml_file_path: str) -> str:
    """Checks if JSON data from a file is valid according to a schema from a YAML file.

    Args:
        json_file_path: The path to the JSON data file.
        yaml_file_path: The path to the YAML schema file.

    Returns:
        A string indicating whether the JSON data is valid, or an error message.
    """
    try:
        command = ["check-jsonschema", "--schemafile", yaml_file_path, json_file_path]
        result = subprocess.run(command, capture_output=True, text=True, check=False)

        if result.returncode == 0:
            return f"JSON data in '{json_file_path}' is valid according to schema in '{yaml_file_path}'."
        else:
            error_message = result.stderr.strip() if result.stderr else result.stdout.strip()
            return f"Validation Error: JSON data in '{json_file_path}' is NOT valid according to schema in '{yaml_file_path}'. Details: {error_message}"
    except FileNotFoundError:
        return "Error: 'check-jsonschema' command not found. Please ensure it is installed and in your system's PATH."
    except Exception as e:
        return f"An unexpected error occurred: {e}"

if __name__ == "__main__":
    mcp.run(transport="http", port="8080")