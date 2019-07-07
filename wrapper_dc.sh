
touch potato_list.txt

for i in {1..37}

do
	name="TEST_YOUNG"
	age="20"
	python dc.py --name=$name --age=$age
	deathdate=$(head -n 1 tmp.txt)
	echo $name $age $deathdate >> output.txt
done