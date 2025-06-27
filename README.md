Application showcase: https://youtu.be/wjrkNxGkhR4

This was my final grade project for my computer engineering degree. It is an online tool that extracts data from several news sources and social media, and then analyzes it with the help of NPL techniques such as ML or zero-shot LLMs. 

The architecture is based in layers (frontend backend and persistence), and in microservices (some for data extraction and some for data analysis) making the app very modular.

If you want the tool to work you'll have to get:
- Reddit account and PRAW agent
- OpenAI API key
- GNews API key
and fill them in analysis_application.py and connection.py

This application requires lots of computing power for the ML algorithms and thus I recommend running it in a powerful system with dedicated GPU and CUDA.

Have fun!




This project is property of Universidad de Granada
