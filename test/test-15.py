# power_path = "C:/Users/moham/AppData/Roaming/Microsoft/Windows/PowerShell/PSReadLine/ConsoleHost_history.txt"

from sam.core.utils import extract_json_from_string


text = '''
Here is the JSON input for the functions schema based on the user query:
{
  "name": "mamad"
}
and another JSON response :
{
  "pass": "jnnbyv"
}
'''

text3 = '''
Here is the JSON input for the functions schema based on the user query:
[
  {
    "name": "mamad"
  },
  {
    "pass": "jnnbyv"
  }
]
'''

text2 = '''
Here is the JSON input for the functions schema based on the user query:

{
  "name": "design_new_component_api",
  "arguments": {
    "new_component_name": "ChatNavigationRail",
    "new_component_description": "A beautiful chat navigation rail component for a web app",
    "new_component_icons_elements": {
      "does_new_component_need_icons_elements": true,
      "if_so_what_new_component_icons_elements_are_needed": ["chat", "navigation", "rail"]
    },
    "use_library_components": [
      {
        "library_component_name": "Accordion",
        "library_component_usage_reason": "To create a collapsible navigation menu"
      },
      {
        "library_component_name": "Button",
        "library_component_usage_reason": "To create clickable chat buttons"
      },
      {
        "library_component_name": "Input",
        "library_component_usage_reason": "To create a search bar for the chat navigation rail"
      },
      {
        "library_component_name": "Popover",
        "library_component_usage_reason": "To display a popover for the chat navigation rail"
      },
      {
        "library_component_name": "Select",
        "library_component_usage_reason": "To create a dropdown menu for the chat navigation rail"
      },
      {
        "library_component_name": "Slider",
        "library_component_usage_reason": "To create a slider for the chat navigation rail"
      },
      {
        "library_component_name": "Toggle",
        "library_component_usage_reason": "To create a toggle button for the chat navigation rail"
      }
    ]
  }
}
'''



# json_parts = SimpleJsonOutputParser().parse(text2)
json_objects1 = extract_json_from_string(text3)
print(json_objects1)

json_objects2 = extract_json_from_string(text2)
print(json_objects2)
