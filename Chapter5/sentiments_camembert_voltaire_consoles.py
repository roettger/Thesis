import tensorflow as tf
from transformers import TFCamembertForSequenceClassification, CamembertTokenizer
import matplotlib.pyplot as plt
from collections import defaultdict

# Loading CamemBERT-Modells & Tokenizers
model_name = "jplu/tf-camembert-base"
tokenizer = CamembertTokenizer.from_pretrained(model_name)
model = TFCamembertForSequenceClassification.from_pretrained(model_name)

# Voltaire: The Two Comforters (Les Deux Consolés)

text = """
 Le grand philosophe Citophile disait un jour à une femme désolée, et qui avait juste sujet de l'être : « Madame, la reine d'Angleterre, fille du grand Henri IV, a été aussi malheureuse que vous : on la chassa de ses royaumes ; elle fut près de périr sur l'Océan par les tempêtes ; elle vit mourir son royal époux sur l'échafaud. 
--- J'en suis fâchée pour elle, dit la dame ; » et elle se mit à pleurer ses propres infortunes. 
« Mais, dit Citophile, souvenez-vous de Marie Stuart : elle aimait fort honnêtement un brave musicien qui avait une très-belle basse-taille. Son mari tua son musicien à ses yeux ; et ensuite sa bonne amie et sa bonne parente, la reine Élisabeth, qui se disait pucelle, lui fit couper le cou sur un échafaud tendu de noir, après l'avoir tenue en prison dix-huit années. 
--- Cela est fort cruel, répondit la dame ; » et elle se replongea dans sa mélancolie. 
« Vous avez peut-être entendu parler, dit le consolateur, de la belle Jeanne de Naples, qui fut prise et étranglée ? 
--- Je m'en souviens confusément, » dit l'affligée. 
« Il faut que je vous conte, ajouta l'autre, l'aventure d'une souveraine qui fut détrônée de mon temps après souper, et qui est morte dans une île déserte. 
--- Je sais toute cette histoire, » répondit la dame. 
« Eh bien donc, je vais vous apprendre ce qui est arrivé à une autre grande princesse à qui j'ai montré la philosophie. Elle avait un amant, comme en ont toutes les grandes et belles princesses. Son père entra dans sa chambre, et surprit l'amant, qui avait le visage tout en feu et l'œil étincelant comme une escarboucle ; la dame aussi avait le teint fort animé. Le visage du jeune homme déplut tellement au père qu'il lui appliqua le plus énorme soufflet qu'on eût jamais donné dans sa province. L'amant prit une paire de pincettes et cassa la tête au beau-père, qui guérit à peine, et qui porte encore la cicatrice de cette blessure. L'amante, éperdue, sauta par la fenêtre et se démit le pied ; de manière qu'aujourd'hui elle boite visiblement, quoique d'ailleurs elle ait la taille admirable. L'amant fut condamné à la mort pour avoir cassé la tête à un très-grand prince. Vous pouvez juger de l'état où était la princesse quand on menait pendre l'amant. Je l'ai vue longtemps lorsqu'elle était en prison ; elle ne me parlait jamais que de ses malheurs. 
--- Pourquoi ne voulez-vous donc pas que je songe aux miens ? lui dit la dame. 
--- C'est, dit le philosophe, parce qu'il n'y faut pas songer, et que, tant de grandes dames ayant été si infortunées, il vous sied mal de vous désespérer. 
Songez à Hécube, songez à Niobé. 
--- Ah  dit la dame, si j'avais vécu de leur temps, ou de celui de tant de belles princesses, et si pour les consoler vous leur aviez conté mes malheurs, pensez-vous qu'elles vous eussent écouté ? » 
Le lendemain, le philosophe perdit son fils unique, et fut sur le point d'en mourir de douleur. La dame fit dresser une liste de tous les rois qui avaient perdu leurs enfants, et la porta au philosophe ; il la lut, la trouva fort exacte, et n'en pleura pas moins. Trois mois après il se revirent, et furent étonnés de se retrouver d'une humeur très-gaie. Ils firent ériger une belle statue au Temps, avec cette inscription : À CELUI QUI CONSOLE. 
"""

# Tokenisierung des Textes
inputs = tokenizer(text.split("---"), return_tensors="tf", padding=True, truncation=True)

# Durchführung der Emotionsanalyse für jeden Satz
outputs = model(inputs)
predicted_labels = tf.argmax(outputs.logits, axis=1).numpy()

# Mapping der vorhergesagten Labels auf Emotionen
emotion_mapping = {
    0: "Freude",
    1: "Angst",
    2: "Wut",
    3: "Trauer",
    4: "Überraschung",
}

# Zählen der Emotionen für jeden Satz
emotion_counts = defaultdict(int)
for label in predicted_labels:
    emotion = emotion_mapping[label]
    emotion_counts[emotion] += 1

# Erstellung des Diagramms
plt.figure(figsize=(8, 6))
plt.bar(emotion_counts.keys(), emotion_counts.values(), color='skyblue')

# Hinzufügen von Titel und Beschriftungen
plt.title('Vorhergesagte Emotionen')
plt.xlabel('Emotion')
plt.ylabel('Anzahl')

# Anzeigen des Diagramms
plt.show()
