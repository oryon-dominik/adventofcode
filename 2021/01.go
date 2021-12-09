package main


import (
    "bufio"
    "fmt"
    "os"
    "strconv"
)


func check(e error) {
    if e != nil {
        panic(e)
    }
}


func readLines(path string) ([]int64) {
    file, file_err := os.Open(path)
    check(file_err)
    defer file.Close()

    var lines []int64
    scanner := bufio.NewScanner(file)
    
    for scanner.Scan() {
        scan := scanner.Text()
        in, parse_err := strconv.ParseInt(scan, 10, 64)
        check(parse_err)
        lines = append(lines, in)

    }
    scan_err := scanner.Err()
    check(scan_err)
    return lines
}


func main() {

    lines := readLines("01.data")

    increasing := 0
    for measurement, _ := range lines {
        if measurement > 0 && lines[measurement] > lines[measurement - 1] {
            increasing ++
        }
    }

    fmt.Println("Result:", increasing)
}
