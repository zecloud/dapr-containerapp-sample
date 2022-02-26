namespace dotnetc

open System

type Tweet =
    {
        id_str : string
        text : string
        favorited : bool
        user: user
        retweeted_status : retweeted_status
    }
and user =
    {
        id_str: string
        following: bool
    }
and retweeted_status=
    {
        id_str: string
        favorited : bool
    }
