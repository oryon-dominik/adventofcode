
string rawFile = readFile();

// 
List<char> singleCaloryPackage = new List<char>();
int weightOfRucksack = 0;
bool rememberBreak = false;
int maxCalories = 0;


for (int ii = 0; ii != rawFile.Length; ii++) {

    if (rawFile[ii] == '\n' && rememberBreak) {
        // add higher value to maxCalories, to find the maximum
        maxCalories = maxCalories < weightOfRucksack ? weightOfRucksack : maxCalories;

        // reset values, because we have a new elf
        weightOfRucksack = 0;
        singleCaloryPackage = new List<char>();
        rememberBreak = false;

        continue;
    }

    if (rawFile[ii] == '\n') {  // if we have a new line, we have a new caloryPackage
        // convert singleCaloryPackage add to elf's weightOfRucksack
        weightOfRucksack += calculateCaloryPackage(singleCaloryPackage);

        singleCaloryPackage = new List<char>();
        rememberBreak = true;

        continue;
    }

    // otherwise continue reading the file pointer
    singleCaloryPackage.Add(rawFile[ii]);
    rememberBreak = false;
}


string readFile() {
    return File.ReadAllText(@"./01.data");
}


int calculateCaloryPackage(List<char> singleCaloryPackage) {
    // integer conversion from string list
    int caloryPackage = 0;
    int decimalPlace = 1;
    for (int jj = singleCaloryPackage.Count; jj != 0; jj--) {
        caloryPackage += int.Parse(singleCaloryPackage[jj - 1].ToString()) * decimalPlace;
        decimalPlace = decimalPlace * 10;
    }
    return caloryPackage;
}

Console.WriteLine(maxCalories);
