namespace dotnetc.Controllers

open Microsoft.AspNetCore.Mvc
open Microsoft.Extensions.Logging
open Dapr.Client
open dotnetc

type msgout = { message:Tweet}

[<ApiController>]
[<Route("")>]
type TweetController (logger : ILogger<TweetController>) =    
    inherit ControllerBase()

    [<HttpPost("tweets-binding")>]
    member this.Post([<FromBody>] msg: Tweet )  : IActionResult = 
        let client =DaprClientBuilder().Build()
        client.InvokeBindingAsync<Tweet>("tweetqueuebinding","create",msg)|> Async.AwaitTask |> Async.RunSynchronously

        //printfn "%s" msg.text

        this.Ok()

    [<HttpOptions("tweetsBinding")>]
    member this.Option():IActionResult=
        this.Ok()



