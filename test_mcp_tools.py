from fastmcp import Client
import asyncio
import json
from pathlib import Path

async def test_analyze_file():
    print("\nTesting analyze_file...")
    client = Client("support.py")
    
    # Create a test file
    test_file = Path("test_file.py")
    test_content = """
# This is a comment
def test_function():
    # TODO: implement this
    pass
"""
    test_file.write_text(test_content)
    async with client:
      try:
          result = await client.call_tool("analyze_file", { "request": {"file_path": str(test_file)}})
          print(f"File analysis result: {json.dumps(result.content[0].text, indent=2)}")
          fileAnalysis = json.loads(result.content[0].text)
          assert fileAnalysis["lineCount"] > 0
          assert fileAnalysis["hasTodos"] == True
          assert fileAnalysis["hasFunctions"] == True
          assert fileAnalysis["hasComments"] == True
          print("✅ analyze_file test passed")
      except Exception as e:
          print(f"❌ analyze_file test failed: {str(e)}")
      finally:
          test_file.unlink(missing_ok=True)

async def test_work_log():
    print("\nTesting log_work...")
    client = Client("support.py")
    
    async with client:
      try:
          work_desc = "Testing the MCP server functionality"
          result = await client.call_tool("log_work", { "work": {"description": work_desc}})
          print(f"Work log result: {json.dumps(result.content[0].text, indent=2)}")
          fileAnalysis = json.loads(result.content[0].text)
          assert fileAnalysis["success"] == True
          assert fileAnalysis["description"] == work_desc
          print("✅ log_work test passed")
      except Exception as e:
          print(f"❌ log_work test failed: {str(e)}")

async def test_task_management():
    print("\nTesting task management...")
    client = Client("support.py")
    
    # Clear existing tasks
    f = open("tasks.json", "w")
    f.write("[]")
    f.close()

    async with client:
      try:
          # Test adding a task
          add_result = await client.call_tool("add_task", { "request": {"title": "Test task"}})
          print(f"Add task result: {json.dumps(add_result.content[0].text, indent=2)}")
          fileAnalysis = json.loads(add_result.content[0].text)
          assert fileAnalysis["success"] == True
          task_id = fileAnalysis["task"]["id"]
          
          # Test listing tasks
          list_result = await client.call_tool("list_tasks", {})
          print(f"List tasks result: {json.dumps(list_result.content[0].text, indent=2)}")
          fileAnalysis = json.loads(list_result.content[0].text)
          assert len(fileAnalysis["tasks"]) > 0
          
          # Test completing a task
          complete_result = await client.call_tool("complete_task", { "request": {"task_id": task_id}})
          print(f"Complete task result: {json.dumps(complete_result.content[0].text, indent=2)}")
          fileAnalysis = json.loads(complete_result.content[0].text)
          assert fileAnalysis["success"] == True
          assert fileAnalysis["task"]["status"] == "completed"
          
          print("✅ Task management tests passed")
      except Exception as e:
          print(f"❌ Task management tests failed: {str(e)}")

async def run_all_tests():
    print("Starting MCP server tests...")
    await test_analyze_file()
    await test_work_log()
    await test_task_management()
    print("\nAll tests completed!")

if __name__ == "__main__":
    asyncio.run(run_all_tests())