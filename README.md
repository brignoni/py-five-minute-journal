# The Python Five Minute Journal

A simple Python application inspired by [The Five Minute Journal - Intelligent Change](https://www.intelligentchange.com/products/the-five-minute-journal).

Read the Hashnode article [here](https://brignoni.dev/preview/63c5bd0a7b3b430008b12dd2).

### Installation

```
pip3 install python-dotenv
pip3 install -U Jinja2
```

### Start your daily Five Minute Journal
In the morning run the command. Running it again in the evening will give you a different set of questions.

```
python3 journal.py
```

Your journal markdown files will be saved in the `journals` directory.

```
2022/5MJ-2022-12-31.md
2023/5MJ-2023-01-01.md
2023/5MJ-2023-01-02.md
2023/5MJ-2023-01-02.md
2023/5MJ-2023-01-04.md
2023/5MJ-2023-01-05.md
```

### Example Journal Output

```markdown

Five Minute Journal | Friday, Jan 1 2023

> Dwell on the beauty of life. Watch the stars, and see yourself running with them.
> 
> ~ Marcus Aurelius, Meditations

---
07:55 AM

### I am grateful for...
1. My family
2. My incredible friends
3. The warm bed that a sleep in

### What would make today great?
1. Walk around the park
2. Go to the coffeeshop
3. Publish this blog article

### Daily affirmations
1. I traveled to Portugal
2. I am grateful for everything I have
3. I am a better Software Engineer than yesterday

---
09:05 PM

### Highlights of the day
1. Had breakfast with family
2. Met a friend at the coffeeshop
3. Practiced Portuguese with my language partner

### What did I learn today?
1. New Portuguese vocabulary
2. Completed an AWS hands-on lab
3. Studied for AWS Certified SysOps Admin Associate 

```