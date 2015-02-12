FILE=/tmp/test-service.last
while read in
do
  echo "$in" > $FILE
  echo `cat $FILE`
done
