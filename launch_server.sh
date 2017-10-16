
python update_images.py &
cd images; python -m SimpleHTTPServer 8111  &
cd ../app/; python app.py &
