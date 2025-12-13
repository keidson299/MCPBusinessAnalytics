from fastmcp import FastMCP
import logging

app = FastMCP("Software Development Support MCP Server")

@app.tool()
async def analyze_file():
    print("Test log message to console")

if __name__ == "__main__":
    logger = logging.getLogger(__name__)

    logging.basicConfig(filename="logs/mcpServer.log", level=logging.INFO)

    logger.info("Starting MCP server...")
    app.run(transport="stdio")