while true; do
  echo "Re-starting Django runserver"
  python3 manage.py runserver 0.0.0.0:3011
  sleep 60
done