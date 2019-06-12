%%%-------------------------------------------------------------------
%%% @author gabriele
%%% @copyright (C) 2019, <COMPANY>
%%% @doc
%%%
%%% @end
%%% Created : 03. Jun 2019 21.43
%%%-------------------------------------------------------------------
-module(raft_kv_http_rest_map).
-author("gabriele").

-export([init/2]).
-export([content_types_provided/2]).
-export([map_to_json/2]).

init(Req, Opts) ->
  {cowboy_rest, Req, Opts}.

content_types_provided(Req, State) ->
  {[
    {<<"text/html">>, map_to_json},
    {<<"application/json">>, map_to_json},
    {<<"text/plain">>, map_to_json}
  ], Req, State}.


map_to_json(Req, State) ->
  M = raft_kv:get_map(),
  P = fun({Key, Value}, AccIn) -> lists:append([list_to_binary(Key ++ " - " ++ Value)],
    AccIn) end,
  R = lists:foldl(P, [], M),
  Body = jsx:encode([{<<"Keys - Values">>, R}]),
  {Body, Req, State}.
