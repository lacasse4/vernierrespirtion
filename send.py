from pythonosc import udp_client

ip = "127.0.0.1"   # loop back
port = 7400

client = udp_client.SimpleUDPClient(ip, port)
client.send_message("/", "Hello")