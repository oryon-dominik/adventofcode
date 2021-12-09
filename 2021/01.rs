use std::fs;

fn main() {

    let filename = "01.data";
    let file = fs::read_to_string(filename)
        .expect("Something went wrong reading the file");
    let depths: Vec<i32> = file.split('\n').map(|x| x.parse::<i32>().unwrap()).collect();

    let mut increasing = 0;
    for (measurement, _depth) in depths.iter().enumerate() {
        if measurement > 0 && depths[measurement] > depths[measurement - 1] {
            increasing += 1
        }
    }

    println!("Result: {}", increasing);

}
