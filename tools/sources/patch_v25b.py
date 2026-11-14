import json
p='/home/claude/appespagnol/index.html';h=open(p,encoding='utf8').read()
def rep(a,b):
    global h
    assert h.count(a)==1,(a[:70],h.count(a));h=h.replace(a,b)
J=lambda x:json.dumps(x,ensure_ascii=False)
U=[
 dict(id='estacion',es='En la estación',fr='Prendre le train',e='🚆',
  words=[['un billete para Madrid','un billet pour Madrid','🎟️'],['ida y vuelta','aller-retour','🔁'],['¿a qué hora sale el tren?','à quelle heure part le train ?','🕐'],
   ['el andén','le quai','🛤️'],['el tren llega tarde','le train arrive en retard','⏰'],['la maleta','la valise','🧳'],['mi asiento','ma place','🪑'],
   ['¿está libre este asiento?','cette place est libre ?','💬'],['el revisor','le contrôleur','👨'],['¡buen viaje!','bon voyage !','👋']],
  talk=[dict(l='¡Hola! ¿Adónde vas?',f='Bonjour ! Où vas-tu ?',p='🚆',o=[['Un billete para Madrid, por favor.',"Un billet pour Madrid, s'il vous plaît.",1],['Un billete para la sopa.','Un billet pour la soupe.',0]]),
   dict(l='¿Solo ida o ida y vuelta?',f='Aller simple ou aller-retour ?',p='🔁',o=[['Ida y vuelta. ¿A qué hora sale el tren?','Aller-retour. À quelle heure part le train ?',1],['Ida y helado, gracias.','Aller et glace, merci.',0]]),
   dict(l='Sale a las diez, del andén tres.',f='Il part à dix heures, du quai trois.',p='🕐',o=[['Muchas gracias. ¿Dónde está el andén tres?','Merci beaucoup. Où est le quai trois ?',1],['Tengo diez andenes en la maleta.',"J'ai dix quais dans la valise.",0]]),
   dict(l='Perdona, ¿está libre este asiento?',f='Pardon, cette place est libre ?',p='🪑',o=[['Sí, está libre. Siéntate.','Oui, elle est libre. Assieds-toi.',1],['Sí, es mi abuela.',"Oui, c'est ma grand-mère.",0]]),
   dict(l='¡Billetes, por favor!',f="Les billets, s'il vous plaît !",p='🎟️',o=[['Aquí tiene mi billete.','Voici mon billet.',1],['Aquí tiene mi pijama.','Voici mon pyjama.',0]])],
  gaps=[['Un _ para Madrid, por favor.','billete',['tren','andén'],'🎟️'],['¿A qué hora _ el tren?','sale',['come','duerme'],'🕐'],['El tren llega _.','tarde',['pronto','grande'],'⏰']]),
 dict(id='biblioteca',es='En la biblioteca',fr='À la bibliothèque',e='📚',
  words=[['la biblioteca','la bibliothèque','📚'],['un libro de piratas','un livre de pirates','🏴‍☠️'],['el carné','la carte de bibliothèque','💳'],
   ['¿puedo llevarme este libro?','je peux emprunter ce livre ?','📖'],['tienes dos semanas','tu as deux semaines','📅'],['hay que devolverlo','il faut le rendre','📆'],
   ['hablar bajito','parler tout bas','🤫'],['el cuento','le conte','📕'],['los cómics','les BD','💥'],['la bibliotecaria','la bibliothécaire','👩']],
  talk=[dict(l='¡Hola! Esta es la biblioteca. Aquí hay que hablar bajito.',f='Bonjour ! Voici la bibliothèque. Ici, il faut parler tout bas.',p='🤫',o=[['Vale. Busco un libro de piratas.',"D'accord. Je cherche un livre de pirates.",1],['Vale. Busco una piscina.',"D'accord. Je cherche une piscine.",0]]),
   dict(l='Los libros de piratas están allí, con los cómics.',f='Les livres de pirates sont là-bas, avec les BD.',p='🏴‍☠️',o=[['¡Gracias! ¿Puedo llevarme este libro?','Merci ! Je peux emprunter ce livre ?',1],['¡Gracias! ¿Puedo comerme este libro?','Merci ! Je peux manger ce livre ?',0]]),
   dict(l='Claro. ¿Tienes tu carné?',f='Bien sûr. Tu as ta carte de bibliothèque ?',p='💳',o=[['Sí, aquí tienes mi carné.','Oui, voici ma carte.',1],['Sí, aquí tienes mi perro.','Oui, voici mon chien.',0]]),
   dict(l='Muy bien. Tienes dos semanas para leerlo.',f='Très bien. Tu as deux semaines pour le lire.',p='📅',o=[['¿Y luego hay que devolverlo?','Et après, il faut le rendre ?',1],['¿Y luego hay que bailarlo?','Et après, il faut le danser ?',0]]),
   dict(l='Sí, el día catorce. ¡Que lo disfrutes!',f='Oui, le quatorze. Bonne lecture !',p='📖',o=[['¡Gracias! ¡Hasta pronto!','Merci ! À bientôt !',1],['¡Gracias! ¡Feliz cumpleaños, libro!','Merci ! Joyeux anniversaire, livre !',0]])],
  gaps=[['Busco un libro de _.','piratas',['zapatos','sopas'],'🏴‍☠️'],['Aquí hay que hablar _.','bajito',['grande','rojo'],'🤫'],['Tienes dos _ para leerlo.','semanas',['manzanas','mesas'],'📅']]),
]
def unit_js(u):
    talk=','.join('{l:%s,f:%s,p:%s,o:%s}'%(J(d['l']),J(d['f']),J(d['p']),J(d['o'])) for d in u['talk'])
    return '{id:%s,tier:3,es:%s,fr:%s,e:%s,words:%s,talk:[%s],gaps:%s}'%(J(u['id']),J(u['es']),J(u['fr']),J(u['e']),J(u['words']),talk,J(u['gaps']))
rep("insAfter('insectos',V9_1);insAfter('emociones',V9_2);UNITS.push(...V9_3);",
 "insAfter('insectos',V9_1);insAfter('emociones',V9_2);UNITS.push(...V9_3);\n/* Version 25 : 2 leçons pour compléter le Niveau 11 « Se débrouiller » (offre Ultimate) */\nconst V25=[\n "+',\n '.join(unit_js(u) for u in U)+"];\nUNITS.push(...V25);")
fr_extra={'¿A qué hora sale el tren?':'À quelle heure part le train ?','El tren llega tarde.':'Le train arrive en retard.',
 'Busco un libro de piratas.':'Je cherche un livre de pirates.','Aquí hay que hablar bajito.':'Ici, il faut parler tout bas.','Tienes dos semanas para leerlo.':'Tu as deux semaines pour le lire.'}
rep("const FR_EXTRA={","const FR_EXTRA={\n "+',\n '.join(J(k)+':'+J(v) for k,v in fr_extra.items())+",")
rep("const ABSTRACT=new Set([","const ABSTRACT=new Set(['¿está libre este asiento?',")
T={'En la estación':['Taking the train','Prendere il treno'],'En la biblioteca':['At the library','In biblioteca'],
 'un billete para Madrid':['a ticket to Madrid','un biglietto per Madrid'],'ida y vuelta':['return (there and back)','andata e ritorno'],'¿a qué hora sale el tren?':['what time does the train leave?','a che ora parte il treno?'],
 'el andén':['the platform','il binario'],'el tren llega tarde':['the train is late','il treno è in ritardo'],'la maleta':['the suitcase','la valigia'],'mi asiento':['my seat','il mio posto'],
 '¿está libre este asiento?':['is this seat free?','è libero questo posto?'],'el revisor':['the ticket inspector','il controllore'],'¡buen viaje!':['have a good trip!','buon viaggio!'],
 '¡Hola! ¿Adónde vas?':['Hello! Where are you going?','Ciao! Dove vai?'],'Un billete para Madrid, por favor.':['A ticket to Madrid, please.','Un biglietto per Madrid, per favore.'],'Un billete para la sopa.':['A ticket to the soup.','Un biglietto per la zuppa.'],
 '¿Solo ida o ida y vuelta?':['Single or return?','Solo andata o andata e ritorno?'],'Ida y vuelta. ¿A qué hora sale el tren?':['Return. What time does the train leave?','Andata e ritorno. A che ora parte il treno?'],'Ida y helado, gracias.':['There and ice cream, thanks.','Andata e gelato, grazie.'],
 'Sale a las diez, del andén tres.':['It leaves at ten, from platform three.','Parte alle dieci, dal binario tre.'],'Muchas gracias. ¿Dónde está el andén tres?':['Thank you very much. Where is platform three?','Grazie mille. Dov’è il binario tre?'],'Tengo diez andenes en la maleta.':['I have ten platforms in my suitcase.','Ho dieci binari nella valigia.'],
 'Perdona, ¿está libre este asiento?':['Excuse me, is this seat free?','Scusa, è libero questo posto?'],'Sí, está libre. Siéntate.':["Yes, it's free. Sit down.",'Sì, è libero. Siediti.'],'Sí, es mi abuela.':["Yes, it's my grandma.",'Sì, è mia nonna.'],
 '¡Billetes, por favor!':['Tickets, please!','Biglietti, per favore!'],'Aquí tiene mi billete.':["Here's my ticket.",'Ecco il mio biglietto.'],'Aquí tiene mi pijama.':["Here are my pyjamas.",'Ecco il mio pigiama.'],
 '¿A qué hora sale el tren?':['What time does the train leave?','A che ora parte il treno?'],'El tren llega tarde.':['The train is late.','Il treno è in ritardo.'],
 'la biblioteca':['the library','la biblioteca'],'un libro de piratas':['a book about pirates','un libro di pirati'],'el carné':['the library card','la tessera'],
 '¿puedo llevarme este libro?':['can I borrow this book?','posso prendere in prestito questo libro?'],'tienes dos semanas':['you have two weeks','hai due settimane'],'hay que devolverlo':['you have to bring it back','bisogna restituirlo'],
 'hablar bajito':['speak quietly','parlare piano'],'el cuento':['the story','la fiaba'],'los cómics':['the comics','i fumetti'],'la bibliotecaria':['the librarian','la bibliotecaria'],
 '¡Hola! Esta es la biblioteca. Aquí hay que hablar bajito.':['Hello! This is the library. Here you have to speak quietly.','Ciao! Questa è la biblioteca. Qui bisogna parlare piano.'],
 'Vale. Busco un libro de piratas.':["OK. I'm looking for a book about pirates.",'Va bene. Cerco un libro di pirati.'],'Vale. Busco una piscina.':["OK. I'm looking for a swimming pool.",'Va bene. Cerco una piscina.'],
 'Los libros de piratas están allí, con los cómics.':['The pirate books are over there, with the comics.','I libri di pirati sono lì, con i fumetti.'],
 '¡Gracias! ¿Puedo llevarme este libro?':['Thanks! Can I borrow this book?','Grazie! Posso prendere in prestito questo libro?'],'¡Gracias! ¿Puedo comerme este libro?':['Thanks! Can I eat this book?','Grazie! Posso mangiare questo libro?'],
 'Claro. ¿Tienes tu carné?':['Of course. Do you have your library card?','Certo. Hai la tua tessera?'],'Sí, aquí tienes mi carné.':["Yes, here's my card.",'Sì, ecco la mia tessera.'],'Sí, aquí tienes mi perro.':["Yes, here's my dog.",'Sì, ecco il mio cane.'],
 'Muy bien. Tienes dos semanas para leerlo.':['Very good. You have two weeks to read it.','Molto bene. Hai due settimane per leggerlo.'],'¿Y luego hay que devolverlo?':['And then I have to bring it back?','E poi bisogna restituirlo?'],'¿Y luego hay que bailarlo?':['And then I have to dance it?','E poi bisogna ballarlo?'],
 'Sí, el día catorce. ¡Que lo disfrutes!':['Yes, on the fourteenth. Enjoy it!','Sì, il quattordici. Buona lettura!'],'¡Gracias! ¡Hasta pronto!':['Thanks! See you soon!','Grazie! A presto!'],'¡Gracias! ¡Feliz cumpleaños, libro!':['Thanks! Happy birthday, book!','Grazie! Buon compleanno, libro!'],
 'Busco un libro de piratas.':["I'm looking for a book about pirates.",'Cerco un libro di pirati.'],'Aquí hay que hablar bajito.':['Here you have to speak quietly.','Qui bisogna parlare piano.'],'Tienes dos semanas para leerlo.':['You have two weeks to read it.','Hai due settimane per leggerlo.']}
rep("const TRX={","const TRX={"+','.join(J(k)+':'+J(v) for k,v in T.items())+",")
open(p,'w',encoding='utf8').write(h);print('ok')
