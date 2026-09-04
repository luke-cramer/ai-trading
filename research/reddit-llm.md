# Reddit sweep: LLM-trading experiments and opinions — BLOCKED (API saturation)

**Status: incomplete.** This beat could not be executed this session. Zero posts or comments
were retrieved from Reddit. Every finding below is a diagnostic record of *why*, not a synthesis
of Reddit content — there is no Reddit content to synthesize. Do not cite this file as evidence
about LLM-trading sentiment; it is evidence only about tooling availability. Flagging this clearly
per method requirements rather than fabricating permalinks, quotes, or usernames to fill the gap.

## What was required

Per the assigned beat: sweep r/algotrading, r/ChatGPT, r/ClaudeAI, r/OpenAI, r/LocalLLaMA,
r/wallstreetbets, r/CryptoCurrency and related subs for real-money LLM-trading experiment
reports (with outcomes, not just launches), vibe-coded trading-bot horror stories/wins,
LLM-on-news/social sentiment-signal builders, and community consensus — via
`~/.claude/skills/reddit/reddit.py` against the Arctic Shift archive API, per
`~/.claude/skills/reddit/SKILL.md`.

## What was attempted

Read the skill file first, confirmed correct invocation via `--help`, then ran (in order):

1. `subs algotrategy` (typo aside) / `subs algotrading` — direct subreddit lookup, no query.
2. `search "ChatGPT trading" --sub algotrading --after none --min-comments 5`
3. `search "ChatGPT" --sub algotrading --after none --min-comments 5` (single-term control)
4. `subs algotrading` again (isolate whether `search`'s params were the problem — they weren't)
5. `subs LocalLLaMA` (rule out a subreddit-name-specific issue)
6. `thread https://reddit.com/r/algotrading/comments/1arkr9d/` and `thread 1arkr9d` (different
   endpoint entirely — `/posts/ids` + `/comments/tree` — to rule out `/posts/search` specifically
   being broken)

**Every one of the six calls above returned `HTTP 500` — `{"data":null,"error":"Internal server
error"}` — immediately**, across four distinct API endpoints (`/subreddits/search`,
`/posts/search`, `/posts/ids`), four different subreddits, with and without a query string, with
and without date filters. This rules out a malformed request on my end; the failure is generic
and endpoint-agnostic.

Cross-checked `https://status.arctic-shift.photon-reddit.com` via WebFetch: it reported the API as
"Available" with no listed outage — the status page is not a reliable signal of the load-induced
500s actually being served; treat it as uninformative here, not as evidence the API was fine.

### Root cause identified: machine-wide contention, not a bug in this query

`reddit.py` serializes every request **across every Claude session running on this machine**
through one `flock`-protected state file (`~/.cache/reddit-skill/lock`), with a 3-second minimum
gap between requests globally, and shared exponential backoff (5/10/20/40/60s) triggered by
upstream 429/503/422 responses from *any* session's request. `ListAgents` showed **19 other
concurrent interactive sessions** on this machine (unrelated projects — `yourfan-*`,
`picklemate-*`, `creator-tools`, `dupr-multi-check`, etc.), and a live process scan
(`pgrep -f "reddit.py search"`) found the *reddit.py search* subcommand alone running
concurrently **53, then 78, processes deep** at two check points roughly 5 minutes apart — i.e.
the shared queue was *growing*, not draining, over the course of this session's attempts. Sample
competing invocations pulled from `ps`: unrelated searches for `"banned"`, `"cam4"`,
`"streamate"`, `"fanbox"`, `"niteflirt"`, `"twitcasting"` running in parallel with mine — confirms
this is cross-tenant load on a single community-run, single-threaded-by-design backend, not
anything specific to trading-related queries.

Lock-file state samples taken during the session showed `strikes` cycling 2→3→4 and
`cooldown_until` repeatedly extending 20–58s into the future as other sessions' requests kept
tripping 429/503/500 faster than the shared backoff could clear — a classic thundering-herd
pattern against a small community API (per the skill's own caveat: "Community-run research API
with no uptime guarantee").

Concretely, my actual target query —
`search "ChatGPT trading" --sub algotrading --after none --min-comments 3 --limit 20`
— was launched, entered the shared retry loop, and was **still running with zero output after
8+ minutes of wall-clock time** (`ps -p <pid> -o etime=` → `08:00`), by which point the
machine-wide `reddit.py search` process count had grown to 78. At that point I stopped waiting
per the skill's explicit guidance: *"A run that ends in HTTP 429/422 after retries means the API
is saturated: stop Reddit work for that turn, say so, and rely on what you already have."* I have
nothing to rely on — the honest report is that this beat returned no data.

Also relevant: this session's `WebSearch` tool returned "this session has used its web search
budget (200 of 200 WebSearch calls)" on the first attempt this session — i.e. a fallback
sweep of web-syndicated Reddit content (news write-ups quoting specific threads, aggregator
sites) via WebSearch was also unavailable, independent of the Reddit-API issue. Per the skill,
`reddit.com` itself blocks direct `WebFetch`/`WebSearch`/`curl`, so there was no secondary path
to reach live Reddit content this session either.

## What was explicitly NOT done

- No posts or comments were read, quoted, or paraphrased from Reddit.
- No permalinks, usernames, dates, upvote counts, or claimed dollar figures are reported below,
  because none were retrieved. Any such details in a companion report from a different beat this
  session should be weighed on their own merits, not assumed to corroborate this one.
- I did not substitute pre-training knowledge dressed up as sourced Reddit content. Where a
  research report needs "community consensus on LLM trading," that gap should be filled by a
  retry of this beat, not by unsourced recall presented as [anon]/[verified] evidence.

## Recommended remediation (for the orchestrator / a retry)

1. **Retry this beat in isolation**, ideally when fewer concurrent sessions are active on this
   machine — the bottleneck is the shared `~/.cache/reddit-skill/lock` file and the single
   community backend's real throughput ceiling, not this task's queries.
2. If retried while load is still high, narrow scope per attempt (one sub, one phrasing, small
   `--limit`) and accept that `thread` calls (which fetch full comment trees) will be the slowest
   and most contention-sensitive — consider running `search` first across sessions to identify
   the 3–6 richest threads, then a single batched `thread` call for those, exactly as the skill
   recommends, rather than iterating.
3. If the orchestrator can serialize/stagger which fan-out beats hit `reddit.py` (rather than all
   researchers across all concurrent projects firing simultaneously), the shared 3-second/request
   ceiling would actually be sufficient — the failure mode here is concurrency, not raw rate
   limits.
4. Planned query set for the retry (unchanged from the original assignment, for reuse):
   - `search "ChatGPT trading"` / `"GPT trade"` / `"Claude trading"` / `"LLM trading bot"` /
     `"AI picked my stocks"` / `"let AI trade"` across `--sub algotrading,ChatGPT,ClaudeAI,
     OpenAI,LocalLLaMA,wallstreetbets,CryptoCurrency` (one sub per call — batching multiple subs
     into one `--sub a,b,c` invocation did not appear to be the cause of the 500s, since
     single-sub calls failed identically, but keep calls small regardless).
   - Follow `mentioned subs:` lines outward once.
   - Pull full `thread` (post + comments) on the 3–6 highest comment+score hits per query.
   - Specifically hunt for thread *endings* (edit logs, "final update," "shutting this down"
     comments) on any real-money LLM-trading experiment thread found, per the assignment's
     emphasis on outcomes over launches.

## Evidence-quality note

Nothing in this file is a claim about LLM trading itself; everything above is [verified] in the
narrow sense that it is directly observed tool/process/API behavior from this session
(`ps`, `pgrep`, cache/lock file contents, raw HTTP response bodies, `ListAgents` output) — cited
inline above rather than in a separate section, since there are no Reddit-content claims to tag.
