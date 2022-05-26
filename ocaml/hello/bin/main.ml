(* This is a series of tail-recursive functions *)
(* 
    nth Fibonacci number
    Print all elements in a list
    Create a list with an arbitrary length and fill
    Sum of the elements in a list
 *)

open Printf
 (* nth Fibonacci number *)
 let rec fib_aux n p pp = 
    if n <= 0 || n >= 8_000 then 
        invalid_arg "n must be greater than - - and less than or equal to 8000"
    
    else if n = 1 then 
        pp 
    
    else 
        fib_aux (n-1) pp (pp+p)

let fib n = 
    fib_aux n 0 1

let n = 50
let () = printf "%ith Fibonacci number %i\n" n (fib n)


(* Sum of a list *)

let rec print_string_of_list ?(first=false) lst = 
    match lst with
        | [] -> ()
        | h :: t -> ( if first then printf "[" ); printf " %i" h; (if t = [] then printf " ]"); print_string_of_list t

let rec sum_aux lst acc = 
    match lst with 
        | [] -> acc
        | h :: t -> sum_aux t (acc + h)

let sum lst = 
    sum_aux lst 0

let rec create_list_aux length fill output = 
    if length = 0 then output 
    else 
        create_list_aux (length-1) fill (fill::output)

let create_list length fill = 
    create_list_aux length fill []
    

let print_fill = 2
let print_length = 10
let print_lst = create_list print_length print_fill
let () = print_string_of_list print_lst ~first:true
let () = printf "\n"

let fill = 1
let length = 10_000_000
let lst = create_list length fill

let () = printf "Sum of the elements in "
let () = printf "%i:%i" fill length
let () =  printf ": %i" (sum lst)