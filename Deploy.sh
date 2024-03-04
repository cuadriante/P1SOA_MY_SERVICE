echo "Please input your OPENAI_API_KEY: "
read OPENAI_API_KEY
chmod 400 VM_KEY/Recommendation_Key.pem
scp -i VM_KEY/Recommendation_Key.pem -rp *  ubuntu@ec2-34-208-253-148.us-west-2.compute.amazonaws.com:SOA
ssh -i VM_KEY/Recommendation_Key.pem ubuntu@ec2-34-208-253-148.us-west-2.compute.amazonaws.com "
export PATH=\"\$PATH:/home/ubuntu/.local/bin\"
export OPENAI_API_KEY=\"$OPENAI_API_KEY\"
sudo apt-get update
sudo apt install -y python3-pip nginx
pip install fastapi uvicorn python-dotenv openai requests
cd SOA
sudo cp recommendation_nginx /etc/nginx/sites-enabled/
sudo service nginx restart
cd app
uvicorn main:app --reload
"