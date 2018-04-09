# arg1 = Number of clients
# arg2 = Starting port number

for i in $(seq 1 $1); do
  PORT=$(($2 + $i - 1))
  echo "Launching client $i on port $PORT"
  python client_multi.py $PORT &
done
# if [ "$2" = 1 ]; then
#   echo "Launching profile spammer"
#   python client_spammer_with_profiling.py
# fi
