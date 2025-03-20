import json
import time
from selenium import webdriver
from browsermobproxy import Server

# Start BrowserMob Proxy
server = Server(r"C:\Users\rushi\Downloads\browsermob\browsermob-proxy-2.1.4\bin\browsermob-proxy.bat")
server.start()
proxy = server.create_proxy()



chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument(f"--proxy-server={proxy.proxy}")

# capturing network requests
proxy.new_har("exactspace", options={"captureHeaders": True, "captureContent": True})


driver = webdriver.Chrome(options=chrome_options)
driver.get("https://exactspace.co/")
time.sleep(5)  # Allow some time for requests to complete

# Save the .har file
har_data = proxy.har
with open("network_data.har", "w", encoding="utf-8") as har_file:
    json.dump(har_data, har_file, indent=4)


driver.quit()
server.stop()

print("network_data.har has been saved successfully.")

# Load the .har file
with open("network_data.har", "r", encoding="utf-8") as file:
    har_data = json.load(file)

# Extract HTTP response status codes
status_codes = [entry["response"]["status"] for entry in har_data["log"]["entries"]]


total_requests = len(status_codes)


status_summary = {}
for code in status_codes:
    category = f"{code // 100}XX"
    status_summary[category] = status_summary.get(category, 0) + 1

# Compute percentage breakdown
summary_list = []
for category, count in status_summary.items():
    percentage = round((count / total_requests) * 100, 2)
    summary_list.append({"category": category, "count": count, "percentage": percentage})

# Prepare final JSON output
final_summary = {
    "total_requests": total_requests,
    "status_summary": summary_list
}

# Save to JSON file
with open("network_summary.json", "w", encoding="utf-8") as output_file:
    json.dump(final_summary, output_file, indent=4)

print("network_summary.json has been generated successfully!")
