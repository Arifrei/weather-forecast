import os
from bs4 import BeautifulSoup
import requests as rq
import smtplib
from email.message import EmailMessage
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
data = rq.get("https://www.weather-forecast.com/locations/Monsey/forecasts/latest")
bs = BeautifulSoup(data.text, "html.parser")

def c_to_f(celsius):
    return (celsius * 9/5) + 32

descriptions = [item.text for item in bs.select(".b-forecast__table-summary .b-forecast__text-limit")[:3]]
high_temps = [c_to_f(int(item.text)) for item in bs.select(".b-forecast__table-max-temperature .b-forecast__table-value")[:3]]
low_temps = [c_to_f(int(item.text)) for item in bs.select(".b-forecast__table-min-temperature .b-forecast__table-value")[:3]]
feels_like = [c_to_f(int(item.text)) for item in bs.select(".b-forecast__table-feels .b-forecast__table-value")[:3]]

info = list(zip(descriptions, high_temps, low_temps, feels_like))
am, pm, night = info

sender_email = os.getenv("EMAIL_ADDRESS")
recipient_email = os.getenv("RECIPIENT_EMAIL")
app_password = os.getenv("EMAIL_PASSWORD")

date = datetime.today().strftime("%A %B %d").lstrip("0").replace(" 0", " ")

msg = EmailMessage()
msg["Subject"] = "Today's Weather Forecast"
msg["From"] = sender_email
msg["To"] = recipient_email
msg.set_content(f"""
Weather forecast for {date}

AM:
    Forecast: {am[0]}
    High: {am[1]:.1f}°F
    Low: {am[2]:.1f}°F
    Feel: {am[3]:.1f}°F

PM:
    Forecast: {pm[0]}
    High: {pm[1]:.1f}°F
    Low: {pm[2]:.1f}°F
    Feel: {pm[3]:.1f}°F

Night:
    Forecast: {night[0]}
    High: {night[1]:.1f}°F
    Low: {night[2]:.1f}°F
    Feel: {night[3]:.1f}°F
""")


msg.add_alternative(f"""
<html>
  <body style="font-family: Arial, sans-serif; color: #333;">
    <h2 style="color: #2a7ae2;">Weather Forecast for {date}</h2>

    <h3>Morning (AM)</h3>
    <ul>
      <li><strong>Forecast:</strong> {am[0]}</li>
      <li><strong>High:</strong> {am[1]:.1f}°F</li>
      <li><strong>Low:</strong> {am[2]:.1f}°F</li>
      <li><strong>Feels Like:</strong> {am[3]:.1f}°F</li>
    </ul>

    <h3>Afternoon (PM)</h3>
    <ul>
      <li><strong>Forecast:</strong> {pm[0]}</li>
      <li><strong>High:</strong> {pm[1]:.1f}°F</li>
      <li><strong>Low:</strong> {pm[2]:.1f}°F</li>
      <li><strong>Feels Like:</strong> {pm[3]:.1f}°F</li>
    </ul>

    <h3>Night</h3>
    <ul>
      <li><strong>Forecast:</strong> {night[0]}</li>
      <li><strong>High:</strong> {night[1]:.1f}°F</li>
      <li><strong>Low:</strong> {night[2]:.1f}°F</li>
      <li><strong>Feels Like:</strong> {night[3]:.1f}°F</li>
    </ul>

  </body>
</html>
""", subtype="html")

server = smtplib.SMTP("smtp.gmail.com", 587)
server.starttls()
server.login(user=sender_email, password=app_password)
server.send_message(msg)

server.quit()



