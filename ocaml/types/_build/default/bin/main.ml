type ptype = TNormal | TWater | TFire
type mon = { name: string ; hp: int ; ptype: ptype}

let c = { name = "Charmander"; hp = 100; ptype = TFire }
let () = Printf.printf "%i\n" c.hp

let d = { name = "Charmander2"; hp = 100; ptype = TNormal }
let () = Printf.printf "%i\n" d.hp

let e = { name = "Charmander3"; hp = 100; ptype = TWater }
let () = Printf.printf "%i\n" e.hp

let mon_to_string = function
    | TNormal -> "Normal Type"
    | TWater -> "Water Type"
    | TFire -> "Fire Type"

let print_mon chan m = output_string chan (mon_to_string m)

let get_ptype = function 
    | { ptype=pt; _ } -> pt

let () = Printf.printf "%a\n" print_mon (get_ptype c)

let sum_tuple = function 
    | (x , y, z) -> x + y + z

let a = (1, 2, 3)
let () = Printf.printf "%i\n" (sum_tuple a)


let get_x = fun (x, _) -> x
let get_id = fun x -> x

(* Defining type synonyms *)
type point = float * float
type vector = float list
type matrix = float list list

let p1: point = (1., 2.)
let p2: float * float = (2., 3.)
let v1: vector = [1.;2.;3.;4.;5.]
let m1: matrix = [[1.;2.;3.;4.;5.]; [1.;2.;3.;4.;5.]]

let () = Printf.printf "The first value of the point is %f\n" (get_x p1)
let _ = get_id p1
let _ = get_id p2
let _ = get_id v1
let _ = get_id m1

