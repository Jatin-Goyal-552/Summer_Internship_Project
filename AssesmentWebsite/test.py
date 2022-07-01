import requests
import json

url = "https://summerinternshipproject.pythonanywhere.com/questionbanklevel/"

payload = json.dumps({
  "qlevel": "1"
})
headers = {
  'Content-Type': 'application/json',
  'Cookie': 'csrftoken=25dmhhLvfni2MT5fKWEC6QLXa78TiQQLIov0g0MCjDv4nU6gLmH2xIL3OSvDMBgW; sessionid=trvfjgwt7uxalg81djexqqitaude46va'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
