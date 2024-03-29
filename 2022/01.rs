use std::fs;

fn main() {

    let filename = "2022/01.data";  // TODO: dynamic folder selection
    let file = fs::read_to_string(filename)
        .expect("Something went wrong reading the file");

    let elves: Vec<&str> = file.split("\n\n").collect();
    let weights: Vec<&str> = elves.into_iter().filter(
        (comp![e.parse::<i32>().unwrap(); for e in e.split("\n")]).sum()
    ).collect();

    println!("weights: {:?}", weights);
    // println!("Result: {}", increasing);

}
