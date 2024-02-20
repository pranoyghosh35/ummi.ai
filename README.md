Recommended Step-0:

Create a virtual environment
python -m venv venv

Activate it on Windows:
venv\Scripts\activate
Activate it on macOS and Linux:
source venv/bin/activate

Step-1. pip install -r requirements.txt
Step-2. streamlit run <any_streamlit_app.py>

sample_ui.py is our app selector - so maybe run it first and click at whichever feature you want to use
Each feauture has been developed as an independent streamlit_app described below:

ummi_qa_bot.py     : MaQuery, so that working mothers don't have to use search engine again.
lyrics_selector.py : Lullaby Anytime feature.

Step-3. you can also run standalone python script
ummi_qa_cmd.py : enhanced MaQuery that runs on terminal itself.

