# arg1 = Number of servers
# arg2 = Starting port number
# arg3 = 1 to start a profiler, 0 otherwise

PORT=$2
for i in $(seq 1 $1); do
  # PORT=$(($2 + $i - 1))
  echo "Launching server $i on port $PORT"
  python server_multi.py $PORT &
  PORT=$(($PORT + 1))
done
if [ "$3" = 1 ]; then
  echo "Launching server with profiler"
  python server_multi_with_profiling.py $PORT
fi
