for i in $(seq 1 $1); do
  echo "Launching client $i"
  python client_multi.py &
done
# if [ "$2" = 1 ]; then
#   echo "Launching profile spammer"
#   python client_spammer_with_profiling.py
# fi
