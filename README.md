# Kialo Discussion Parser

A module for parsing exported discussion files from https://www.kialo.com/.

### Usage:


```python
from src.discussiontree import DiscussionTree
```

Create a discussion tree object from a Kialo exported discussion text file:


```python
dt = DiscussionTree("example.csv")
```

Get a node from the tree:


```python
dt.get_entry("1.1.4.")
```




    {'index': '1.1.4.',
     'content': 'Justified belief requires some sort of evidence. Therefore, belief without evidence is unjustified.',
     'stance': 'Con'}



Retrieve the parent of a node


```python
dt.get_parent("1.1.5.")
```




    {'index': '1.1.',
     'content': 'Absence of evidence is not evidence of absence.',
     'stance': 'Con'}



Get the siblings of a node:


```python
dt.get_siblings("1.1.5.")
```




    [{'index': '1.1.1.',
      'content': 'Absence of evidence is enough to be skeptical about a certain proposition.',
      'stance': 'Con'},
     {'index': '1.1.2.',
      'content': 'There are many events in the Bible asserted as false before being evidenced. Exodus being false would be a premature assertion.',
      'stance': 'Pro'},
     {'index': '1.1.3.',
      'content': 'Absence of evidence when evidence is to be expected to be found is a valid form of evidence in itself.',
      'stance': 'Con'},
     {'index': '1.1.4.',
      'content': 'Justified belief requires some sort of evidence. Therefore, belief without evidence is unjustified.',
      'stance': 'Con'}]



Get the children of a node:


```python
dt.get_children("1.1.5.")
```




    [{'index': '1.1.5.1.',
      'content': 'This does not preclude the possibility that there is insufficient evidence to determine if a claim is true or false. Regardless of that fact though, the burden of proof remains that those making the claim must produce evidence to provide sufficient warrant for their position, or to abandon the claim as true citing there is insufficient evidence to consider it as true, which is not an admission that it is false, merely that it is unknown.',
      'stance': 'Con'}]



Get a claim containing a search term (also accepts regular expressions):


```python
indices = dt.find("fallacy")
dt.get_entry(indices[0])["content"]
```




    '[Appeal to ignorance](https://en.wikipedia.org/wiki/Argument_from_ignorance) is a logical fallacy, it should not be asserted that a proposition is true because it has not yet been proven false.'


