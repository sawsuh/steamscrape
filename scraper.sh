cd steam
rm out.json
timeout 60 scrapy crawl steamscrape -o out.json -t json
python jsonInterpret.py > ../out.txt
cd ..
nvim out.txt
