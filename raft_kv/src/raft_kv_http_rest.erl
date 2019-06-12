%%%-------------------------------------------------------------------
%%% @author gabriele
%%% @copyright (C) 2019, <COMPANY>
%%% @doc
%%%
%%% @end
%%% Created : 03. Jun 2019 21.43
%%%-------------------------------------------------------------------
-module(raft_kv_http_rest).
-author("gabriele").

-export([init/2]).
-export([content_types_provided/2]).
-export([members_to_json/2]).

init(Req, Opts) ->
  {cowboy_rest, Req, Opts}.

content_types_provided(Req, State) ->
  {[
    {<<"text/html">>, members_to_json},
    {<<"application/json">>, members_to_json},
    {<<"text/plain">>, members_to_json}
  ], Req, State}.


members_to_json(Req, State) ->
  {Leader, Followers, Nodes} = raft_kv:members_flat(),
  P = fun(A, AccIn) -> lists:append([ra_lib:ra_server_id_node(A)], AccIn) end,
  N = lists:foldl(P, [], Nodes),
  F = lists:foldl(P, [], Followers),
  Body = jsx:encode([{<<"cluster_name">>,<<"--- Erlang Raft Cluster ---">>},
    {<<"leader_node">>, ra_lib:ra_server_id_node(Leader)},
    {<<"node_followers">>, F}, {<<"cluster_nodes">>, N}]),

  {Body, Req, State}.
