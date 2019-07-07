printf_center() {
	title=$1
	C=$(tput cols) 
	printf "%*s" $(((${#title}+$C)/2)) "$title"
}

printf_left() {
	title=$1
	RED='\033[0;31m'
	NC='\033[0m'
	printf "                ${RED}$title${NC}"
}

clear

i="0"
touch output.txt


while [ $i -eq 0 ]; do

	printf "\n\n\n\n"
	printf_center "disInc. Death Clock Generator"
	printf "\n\n"
	bash skull.sh

	printf "\n\n\n\n"
	printf_left "What do your friends call you?: "
	read -r name
	printf "\n"

	printf_left "Hello $name, how many years have you lived?: "
	read -r age
	printf "\n"

	printf_left "And how many years would you like to have lived at the time of your death?: "
	read -r pred_deathage
	printf "\n"

	size=${#myvar} 
	if [ "$size" -lt "1" ]; then
		pred_deathage="0"
	fi

	printf "\n\n"
	printf_center "Give us a moment..."
	printf "\n\n" 
	
	python dc.py --name="$name" --age=$age
	
	COLUMNS=$(tput cols) 
	deathdate=$(head -n 1 tmp.txt)
	deathage=$(tail -n 1 tmp.txt)


	printf "\n\n" 
	num_spaces=$((COLUMNS/2))
	s=$(printf "%-${num_spaces}s" " ")
	echo "${s// /* }" 

	printf "\n\n"
	printf_center "Consider choosing to believe that you will die on:"
	printf "\n\n"

	figlet -c -w $COLUMNS $deathdate

	printf "\n\n"
	printf_center "at the age of: "$deathage""
	printf "\n\n"

	echo "${s// /* }" 
	printf "\n\n"

	printf_left "Would you like to invest? [y/n]: "
	read -r invest

	if [ "$invest" = "y" ]; then

		printf_left "How much US currency do you intend to invest upon receipt of your product?: $"
		read -r amount
		printf "\n\n\n"
		printf_center "Please consult with the local disInc. representative to complete your transaction"
	else
		amount="N/A"
	fi

	printf "$name \t $age \t $pred_deathage \t $deathdate \t $deathage \t $invest \t $amount\n" >> output.txt

	printf "\n\n" 
	r=`expr $deathage - $age`
	printf_center "Enjoy your $r remaining years!"
	printf "\n\n"
	printf_center "We love you."
	printf "\n\n\n\n"
    printf_center "Press 'ENTER' for new customer: "
    read exit

    

    if [ "$exit" = "q" ]; then
		i="1"
	fi

	clear


done