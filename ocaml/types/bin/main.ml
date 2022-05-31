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

type pmon_or_ptype = 
    | Pmon of pmon
    | Ptype of ptype

type battle = {
    attacker: pmon_or_ptype;
    defender: pmon_or_ptype;
}

let get_ptype = function 
    | Pmon p -> p.ptype
    | Ptype p -> p

let effect_of_battle bat = 
    let attacker_type = get_ptype bat.attacker in 
    let defender_type = get_ptype bat.defender in 
    match attacker_type, defender_type with 
        | TNormal, _ | _, TNormal
            -> ENormal
        | TFire, TFire | TWater, TWater | TFire, TWater
            -> ENotVery
        | TWater, TFire 
            -> ESuper

let mult_of_effect = function 
    | ENormal -> 1.
    | ENotVery -> 0.5
    | ESuper -> 2.