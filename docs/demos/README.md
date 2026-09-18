# Side-by-side labs

**Time:** 20 to 30 minutes each
**You will learn:** what instructions, skills, and agents actually change about Copilot's output
**You will need:** lesson 03 finished

The lessons explain what these three things are. The labs make you watch the
same prompt produce two different answers, with and without them.

Do them. Nobody believes a customization file matters until they have seen one
prompt return a defensible paragraph in one window and confident nonsense in the
other. Reading about it does not work.

## How the labs are set up

You run every lab prompt twice:

- In **collateral-iq-baseline**, a stripped copy with identical code and data and
  no customization at all.
- In **collateral-iq**, the real repository.

Then you compare what came back.

Build the baseline once, from the real repository:

```bash
python tools/make_baseline.py
```

It writes `../collateral-iq-baseline/` as a sibling folder. That placement is
deliberate: VS Code loads `.github/copilot-instructions.md` from the root of the
folder you have open, so a baseline nested inside this repo would still inherit
our instructions and the comparison would be worthless.

Open it in a **separate VS Code window**. Arrange the two windows side by side if
your screen allows. Then confirm the control group is genuinely a control -
in the baseline window, ask Copilot Chat:

> What rules am I supposed to follow when writing code in this repository?

You should get generic advice about clean code. If you get our vocabulary, you
are in the wrong window and every result after this will be meaningless.

## The three labs

| Lab | Isolates | Pairs with |
| --- | --- | --- |
| [Lab 1 - Instructions](lab-1-instructions.md) | `copilot-instructions.md` and scoped `.instructions.md` | [Lesson 04](../04-instructions.md) |
| [Lab 2 - Skills](lab-2-skills.md) | `SKILL.md` and its bundled script | [Lesson 05](../05-skills.md) |
| [Lab 3 - Agents](lab-3-agents.md) | `.agent.md` and its tool boundary | [Lesson 06](../06-agents.md) |

Each lab isolates one variable. That is the whole design: if you turn everything
on at once you learn that "Copilot got better", which teaches you nothing about
which file to write when you hit this problem at work.

## Recording what you get

Copy `results/TEMPLATE.md` to `results/<your-name>-lab-<n>.md` and paste both
outputs in. Two reasons this is worth the two minutes:

1. Model behaviour drifts. A lab that produced a stark difference in March may
   produce a subtler one in September, and the recorded results are how you
   notice rather than assuming you set something up wrong.
2. In the group session, four people's results side by side make the point far
   better than one person's. Especially when someone's baseline output happens
   to come out fine - which it sometimes will, and which is itself worth
   discussing.

## A warning about what you are measuring

These are language models. Run the same prompt twice in the same window and you
will get two different answers. One run proves nothing.

Run each prompt **three times in each window** before concluding anything, and
judge on the pattern rather than the single best or worst result. If the
difference only shows up in one run out of three, the honest finding is that the
customization helped a little, not that it transformed anything - and you should
write that down.

Being straight about this is the most useful habit the labs teach. The point is
not to prove that our setup works. The point is to find out how much it works,
so you know what to rely on.
