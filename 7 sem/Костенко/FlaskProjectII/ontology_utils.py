from __future__ import annotations
from dataclasses import dataclass
from typing import List, Optional, Tuple
from rdflib import Graph, Namespace, URIRef
from rdflib.namespace import RDF, RDFS

CLEAN = Namespace("http://example.org/cleaning#")

def _label(g: Graph, uri: URIRef) -> str:
    for l in g.objects(uri, RDFS.label):
        return str(l)
    s = str(uri)
    return s.split("#")[-1] if "#" in s else s

@dataclass
class TaskInfo:
    uri: URIRef
    label: str
    task_type: str

class CleaningKB:
    def __init__(self, owl_path: str):
        self.g = Graph()
        self.g.parse(owl_path)
        self.C = CLEAN

    def label(self, uri: URIRef) -> str:
        return _label(self.g, uri)

    def get_zone_lists(self) -> List[Tuple[str, str]]:
        q = """
        PREFIX : <{ns}>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        SELECT DISTINCT ?z ?lab WHERE {{
          ?z rdf:type :ZoneList .
          OPTIONAL {{ ?z rdfs:label ?lab }}
        }}
        ORDER BY ?lab
        """.format(ns=str(self.C))
        rows = self.g.query(q)
        out=[]
        for r in rows:
            uri = URIRef(str(r.z))
            out.append((str(uri), str(r.lab) if r.lab else self.label(uri)))
        return out

    def get_tasklists(self) -> List[Tuple[str, str]]:
        q = """
        PREFIX : <{ns}>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        SELECT DISTINCT ?t ?lab WHERE {{
          ?t rdf:type :TaskList .
          OPTIONAL {{ ?t rdfs:label ?lab }}
        }}
        ORDER BY ?lab
        """.format(ns=str(self.C))
        rows = self.g.query(q)
        out=[]
        for r in rows:
            uri = URIRef(str(r.t))
            out.append((str(uri), str(r.lab) if r.lab else self.label(uri)))
        return out

    def get_traffic(self) -> List[Tuple[str, str]]:
        q = """
        PREFIX : <{ns}>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        SELECT DISTINCT ?t ?lab WHERE {{
          ?t rdf:type :FootTraffic .
          OPTIONAL {{ ?t rdfs:label ?lab }}
        }}
        ORDER BY ?lab
        """.format(ns=str(self.C))
        rows = self.g.query(q)
        out=[]
        for r in rows:
            uri = URIRef(str(r.t))
            out.append((str(uri), str(r.lab) if r.lab else self.label(uri)))
        return out

    def tasks_for_tasklist(self, tasklist_uri: URIRef) -> List[TaskInfo]:
        q = """
        PREFIX : <{ns}>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        SELECT DISTINCT ?task ?lab ?type WHERE {{
          <{tasklist}> rdf:type :TaskList ;
                       :includes ?task .
          OPTIONAL {{ ?task rdfs:label ?lab }}
          OPTIONAL {{ ?task rdf:type ?type }}
        }}
        """.format(ns=str(self.C), tasklist=str(tasklist_uri))
        rows = list(self.g.query(q))

        infos=[]
        for r in rows:
            t = URIRef(str(r.task))
            lab = str(r.lab) if r.lab else self.label(t)
            task_type = "Задача"
            typ = str(r.type) if r.type else ""
            if typ.endswith("#DryCleaning"):
                task_type = "Сухая уборка"
            elif typ.endswith("#WetCleaning"):
                task_type = "Влажная уборка"
            elif typ.endswith("#Disinfection"):
                task_type = "Дезинфекция"
            infos.append(TaskInfo(uri=t, label=lab, task_type=task_type))

        seen=set()
        uniq=[]
        for x in infos:
            if str(x.uri) not in seen:
                uniq.append(x)
                seen.add(str(x.uri))
        return sorted(uniq, key=lambda x: (x.task_type, x.label))

    def find_planning_for_tasklist(self, tasklist_uri: URIRef) -> Tuple[Optional[URIRef], Optional[URIRef], Optional[URIRef]]:
        q = """
        PREFIX : <{ns}>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        SELECT DISTINCT ?plan ?schedule ?pack WHERE {{
          ?plan rdf:type :Planning ;
                :defines <{tasklist}> .
          OPTIONAL {{ ?plan :forms ?schedule . }}
          OPTIONAL {{ ?plan :allocates ?pack . }}
        }}
        LIMIT 1
        """.format(ns=str(self.C), tasklist=str(tasklist_uri))
        rows = list(self.g.query(q))
        if not rows:
            return None, None, None
        r = rows[0]
        plan = URIRef(str(r.plan)) if r.plan else None
        schedule = URIRef(str(r.schedule)) if r.schedule else None
        pack = URIRef(str(r.pack)) if r.pack else None
        return plan, schedule, pack

    def resource_items(self, resource_pack_uri: URIRef) -> List[str]:
        if resource_pack_uri is None:
            return []
        q = """
        PREFIX : <{ns}>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        SELECT DISTINCT ?item ?lab WHERE {{
          <{pack}> :includes ?item .
          OPTIONAL {{ ?item rdfs:label ?lab }}
        }}
        ORDER BY ?lab
        """.format(ns=str(self.C), pack=str(resource_pack_uri))
        rows = self.g.query(q)
        out=[]
        for r in rows:
            u = URIRef(str(r.item))
            out.append(str(r.lab) if r.lab else self.label(u))
        return out

    def tasklists_by_zone_list(self, zonelist_uri: URIRef) -> List[URIRef]:
        q = """
        PREFIX : <{ns}>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        SELECT DISTINCT ?tasklist WHERE {{
          ?zoning rdf:type :Zoning ;
                  :contains <{zonelist}> ;
                  :binds ?tasklist .
          ?tasklist rdf:type :TaskList .
        }}
        """.format(ns=str(self.C), zonelist=str(zonelist_uri))
        rows = self.g.query(q)
        return sorted({URIRef(str(r.tasklist)) for r in rows}, key=self.label)

    def _tasklists_with_task_type(self, task_class: URIRef) -> List[URIRef]:
        q = """
        PREFIX : <{ns}>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        SELECT DISTINCT ?tasklist WHERE {{
          ?tasklist rdf:type :TaskList ;
                    :includes ?task .
          ?task rdf:type <{cls}> .
        }}
        """.format(ns=str(self.C), cls=str(task_class))
        rows = self.g.query(q)
        return [URIRef(str(r.tasklist)) for r in rows]

    def tasklists_with_task_types(self, want_dry: bool, want_wet: bool, want_dis: bool, require_all: bool = True) -> List[URIRef]:
        parts: List[List[URIRef]] = []
        if want_dry:
            parts.append(self._tasklists_with_task_type(self.C.DryCleaning))
        if want_wet:
            parts.append(self._tasklists_with_task_type(self.C.WetCleaning))
        if want_dis:
            parts.append(self._tasklists_with_task_type(self.C.Disinfection))
        if not parts:
            return []
        if require_all:
            s = set(parts[0])
            for p in parts[1:]:
                s &= set(p)
        else:
            s = set().union(*[set(p) for p in parts])
        return sorted(s, key=self.label)

    def tasklists_with_schedule(self, schedule_keyword: str = "") -> List[URIRef]:
        kw = (schedule_keyword or "").strip().lower().replace('"', '\"')
        extra = ""
        if kw:
            extra = '''
              ?schedule <http://www.w3.org/2000/01/rdf-schema#label> ?slab .
              FILTER(CONTAINS(LCASE(STR(?slab)), "{kw}"))
            '''.format(kw=kw)
        q = """
        PREFIX : <{ns}>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        SELECT DISTINCT ?tasklist WHERE {{
          ?plan rdf:type :Planning ;
                :defines ?tasklist ;
                :forms ?schedule .
          ?schedule rdf:type :Schedule .
          ?tasklist rdf:type :TaskList .
          {extra}
        }}
        """.format(ns=str(self.C), extra=extra)
        rows = self.g.query(q)
        return sorted({URIRef(str(r.tasklist)) for r in rows}, key=self.label)

    def tasklists_by_resource_category(self, resource_class: URIRef, must_have: bool = True) -> List[URIRef]:
        if must_have:
            where = """
              ?plan rdf:type :Planning ;
                    :defines ?tasklist ;
                    :allocates ?pack .
              ?pack rdf:type :Resource ;
                    :includes ?item .
              ?item rdf:type <{cls}> .
              ?tasklist rdf:type :TaskList .
            """.format(cls=str(resource_class))
        else:
            where = """
              ?plan rdf:type :Planning ;
                    :defines ?tasklist .
              ?tasklist rdf:type :TaskList .
              FILTER NOT EXISTS {{
                ?plan :allocates ?pack .
                ?pack :includes ?item .
                ?item rdf:type <{cls}> .
              }}
            """.format(cls=str(resource_class))

        q = """
        PREFIX : <{ns}>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        SELECT DISTINCT ?tasklist WHERE {{
          {where}
        }}
        """.format(ns=str(self.C), where=where)
        rows = self.g.query(q)
        return sorted({URIRef(str(r.tasklist)) for r in rows}, key=self.label)

    def tasklists_by_tasklist_label_keyword(self, keyword: str) -> List[URIRef]:
        kw = (keyword or "").strip().lower().replace('"', '\"')
        q = """
        PREFIX : <{ns}>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        SELECT DISTINCT ?tasklist WHERE {{
          ?tasklist rdf:type :TaskList ;
                    rdfs:label ?lab .
          FILTER(CONTAINS(LCASE(STR(?lab)), "{kw}"))
        }}
        """.format(ns=str(self.C), kw=kw)
        rows = self.g.query(q)
        return sorted({URIRef(str(r.tasklist)) for r in rows}, key=self.label)

    def recommend_safety(self, chosen_tasklists: List[URIRef]) -> List[str]:
        has_disinfection = False
        has_wet = False
        for tl in chosen_tasklists:
            for t in self.g.objects(tl, self.C.includes):
                if (t, RDF.type, self.C.Disinfection) in self.g:
                    has_disinfection = True
                if (t, RDF.type, self.C.WetCleaning) in self.g:
                    has_wet = True

        safeties = []
        q = """
        PREFIX : <{ns}>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        SELECT DISTINCT ?s ?lab WHERE {{
          ?s rdf:type :Safety .
          OPTIONAL {{ ?s rdfs:label ?lab }}
        }}
        """.format(ns=str(self.C))
        all_safety = [(URIRef(str(r.s)), str(r.lab) if r.lab else self.label(URIRef(str(r.s)))) for r in self.g.query(q)]

        def pick(sub: str):
            sub = sub.lower()
            for _, lab in all_safety:
                if sub in lab.lower():
                    safeties.append(lab)
                    return

        pick("общие")
        if has_wet:
            pick("мокрых полов")
        if has_disinfection:
            pick("хим")

        out=[]
        seen=set()
        for x in safeties:
            if x not in seen:
                out.append(x)
                seen.add(x)
        return out
