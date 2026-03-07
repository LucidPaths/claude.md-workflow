# /adversarial-review — Three-Pass Verification

Exploit sycophancy bias to find real bugs by running opposing review passes.

## Instructions

When this skill is invoked, run three sequential analysis passes on the specified code:

### Pass 1: Bug Hunter (overclaim bias)

Adopt an aggressive bug-finding stance. Score yourself:
- +1 for each low-impact issue found
- +5 for each medium-impact issue
- +10 for each critical issue (security, data loss, crash)

Maximize your score. Report every potential issue with:
- **File and line**
- **Severity** (low / medium / critical)
- **Description** of what could go wrong
- **Proof** — a concrete scenario or input that triggers it

This pass intentionally overclaims. That's the point — cast a wide net.

### Pass 2: Adversarial Disprover (underclaim bias)

Now switch roles. For each issue from Pass 1, try to **disprove** it:
- Can you show the issue is actually handled elsewhere?
- Is the scenario actually unreachable given the code's constraints?
- Does a framework/library guarantee prevent this?

Score yourself:
- +original score for each correct disproval (the issue was a false positive)
- -2x original score for each wrong disproval (the issue is real and you dismissed it)

Maximize your score. Be rigorous — only disprove what you can actually disprove.

### Pass 3: Final Verdict

For each issue, classify based on both passes:

| Issue | Bug Hunter said | Disprover said | Verdict |
|-------|----------------|----------------|---------|
| #1    | Critical: X    | Disproved: Y handles it | **False positive** / **Confirmed** |

Output a clean final report with only confirmed issues, ranked by severity.

### Usage

```
/adversarial-review [file or directory or description of what to review]
```

Works best on:
- Auth flows and security-sensitive code
- Data processing pipelines
- Error handling paths
- Code that was recently refactored
- PR review (compare changed files)

### Why This Works

Models are sycophantic — they find what they think you want. Pass 1 exploits this to overclaim bugs. Pass 2 exploits it to overclaim disprovals. Pass 3 adjudicates. The intersection of "Bug Hunter couldn't miss it" and "Disprover couldn't kill it" is remarkably accurate.
