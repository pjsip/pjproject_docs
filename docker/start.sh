if [ -f ~/.bashrc ]; then
  . ~/.bashrc
fi

nohup python3 -m http.server --directory=/root/pjproject_docs/docs/build/html/ 8000 &

