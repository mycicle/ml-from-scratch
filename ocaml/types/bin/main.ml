(* Model of pokemon attack effectiveness *)

type ptype = 
    | TNormal
    | TFire
    | TWater

type peff = 
    | ENormal
    | ENotVery
    | ESuper

type pmon = {
    name: string;
    hp: int;
    ptype: ptype;
}

type battle = {
    attacker: pmon;
    defender: pmon;
}

let effect_of_type attacker_type defender_type = 
    match attacker_type, defender_type with 
        | TNormal, _ | _, TNormal
            -> ENormal
        | TFire, TFire | TWater, TWater | TFire, TWater
            -> ENotVery
        | TWater, TFire 
            -> ESuper

let effect_of_battle bat = 
    let attacker_type = bat.attacker.ptype in 
    let defender_type = bat.defender.ptype in 
    effect_of_type attacker_type defender_type

let mult_of_effect = function 
    | ENormal -> 1.
    | ENotVery -> 0.5
    | ESuper -> 2.

let mult_of_battle bat = bat |> effect_of_battle |> mult_of_effect


let charmander =  { name = "Charmander"; hp = 39; ptype = TFire }
let blastoise = { name = "Blastoise"; hp = 40; ptype = TWater }

(* Manual test *)
(* let () = { attacker = charmander; defender = blastoise } |> mult_of_battle |> string_of_float |> print_endline *)
(* let () = { attacker = blastoise; defender = charmander } |> mult_of_battle |> string_of_float |> print_endline *)


(* Geometry abstractions *)
type point = float * float

type shape = 
    | Circle of { center: point; radius: float }
    | Rectangle of { lower_left: point; upper_right: point }
    | Point of point

let square x = x *. x
let avg x y = (x +. y) /. 2.

(* Requires : If Rectangle, [lower_left = (xll, yll), upper_right = (xur, yur) where xll <= xur and yll <= yur] *)
let get_area = function 
    | Circle { center = _; radius = r} -> 3.14159 *. square r
    | Rectangle { lower_left = (xll, yll); upper_right = (xur, yur)} -> (xur -. xll) *. (yur -. yll)
    | Point _ -> 0.

let get_center = function 
    | Circle {center = c; radius = _ }-> c
    | Rectangle {lower_left = (xll, yll); upper_right = (xur, yur)} -> ((avg xll xur), (avg yll yur))
    | Point p -> p