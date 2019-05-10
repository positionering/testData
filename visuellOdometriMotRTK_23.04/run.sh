./T265/build/pose $1 $2 > test/t265/$3_$1_$2.log &
p1pid=$!
./GPS/build/libsbp_tcp_example -a 192.168.0.222 -p 55555 > test/cord222/$3_$1_222.log &
p2pid=$!
./GPS/build/libsbp_tcp_example -a 192.168.0.223 -p 55555 > test/cord223/$3_$1_223.log &
p3pid=$!

read -n 1 -s -r -p "tryck enter för stänga ner"
echo ""
kill $p1pid $p2pid $p3pid

#paste -d " " test/cord/$2.log test/heading/$2.log > test/concat/$2.log

