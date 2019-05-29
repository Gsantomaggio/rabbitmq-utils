%%%-------------------------------------------------------------------
%%% @author gabriele
%%% @copyright (C) 2019, <COMPANY>
%%% @doc
%%%
%%% @end
%%% Created : 29. May 2019 11.32
%%%-------------------------------------------------------------------
-module(raft_kv_sm).
-behaviour(ra_machine).
-author("gabriele").


-opaque state() :: #{term() => term()}.

-type ra_kv_command() :: {write, Key :: term(), Value :: term()} |
{read, Key :: term()}.
%% API
-export([init/1, apply/3]).

init(_Config) -> #{}.



apply(_Meta, {write, Key, Value},
    #?MODULE{value = Value} = State) ->
  %% no change
  {State, ok, []};
apply(#{index := Idx}, {put, Value},
    #?MODULE{watchers = Watchers, value = OldValue} = State0) ->
  %% notify all watchers of the change of value
  Effects0 = maps:fold(
    fun(P, _, Acc) ->
      [{send_msg, P, {refcell_changed, OldValue, Value}}
        | Acc]
    end, [], Watchers),
  State = State0#?MODULE{value = Value},
  %% emit a release cursor effect every 1000 commands or so
  %% (give or take the number of non state machine commands that ra
  %% processes
  Effects = case Idx rem 1000 of
              0 -> [{release_cursor, Idx, State} | Effects0];
              _ -> Effects0
            end,
  {State, ok, Effects};
apply(_Meta, {write, Key, Value}, State) ->
  {maps:put(Key, Value, State), ok, Effects};
apply(_Meta, {read, Key}, State) ->
  Reply = maps:get(Key, State, undefined),
  {State, Reply, Effects}.



write(Key, Value) ->
  %% it would make sense to cache this to avoid redirection costs when this
  %% server happens not to be the current leader
  Server = ra_kv1,
  case ra:process_command(Server, {write, Key, Value}) of
    {ok, _, _} ->
      ok;
    Err ->
      Err
  end.

read(Key) ->
  Server = ra_kv1,
  case ra:process_command(Server, {read, Key}) of
    {ok, Value, _} ->
      {ok, Value};
    Err ->
      Err
  end.