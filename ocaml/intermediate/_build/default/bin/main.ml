let () = print_endline "Hello, World!"

let rec sum_aux lst acc = 
    match lst with 
        | [] -> acc
        | h :: t -> sum_aux t (acc + h)

(* Returns the sum of the values of the input list. Tail-recursive *)
let sum = function 
    | [] -> 0
    | h::t -> sum_aux t h
