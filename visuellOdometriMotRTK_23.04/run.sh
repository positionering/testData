if [ $# != 2 ] 
then
  echo "2 parametrar, första 1 elr 0 för/ingen odometri, andra namn på log txt"
  exit 128
elif [[ $1 != 0 ]] && [[ $1 != 1 ]]
then
  echo "2 parametrar, första 1 elr 0 för odometri, andra namn på log txt"
  exit 128 
fi

./T265/build/pose-grej $1 > test/t265/$2_$1.log &
p1pid=$!
./GPS/build/libsbp_tcp_example -a 192.168.0.222 -p 55555 > test/cord/$2.log &
p2pid=$!
./GPS/build/libsbp_tcp_example -a 192.168.0.223 -p 55555 > test/heading/$2.log &
p3pid=$!

read -n 1 -s -r -p "tryck enter för stänga ner"
echo ""
kill $p1pid $p2pid $p3pid

paste -d " " test/cord/$2.log test/heading/$2.log > test/concat/$2.log

