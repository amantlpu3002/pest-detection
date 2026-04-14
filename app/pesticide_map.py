"""
pesticide_map.py
----------------
Pest name → recommended pesticide(s) + additional information.
Covers all 102 classes in the IP102 dataset.

Each entry contains:
  pesticides  : list of recommended pesticide names
  type        : chemical class / mode of action
  crop        : affected crop
  severity    : Low | Medium | High
  description : brief description of the pest
  precaution  : safety/application notes
"""

PEST_INFO = {
    # ─── RICE PESTS ──────────────────────────────────────────────────────────
    "rice leaf roller": {
        "pesticides": ["Chlorpyrifos 20 EC", "Monocrotophos 36 SL", "Cartap Hydrochloride 50 SP"],
        "type": "Organophosphate / Nereistoxin analogue",
        "crop": "Rice",
        "severity": "High",
        "description": "Larvae roll rice leaves and feed inside, reducing photosynthesis significantly.",
        "precaution": "Apply in the evening. Avoid during flowering stage."
    },
    "rice leaf caterpillar": {
        "pesticides": ["Chlorantraniliprole 18.5 SC", "Flubendiamide 39.35 SC", "Indoxacarb 14.5 SC"],
        "type": "Diamide / Oxadiazine insecticide",
        "crop": "Rice",
        "severity": "Medium",
        "description": "Caterpillars feed on rice leaves causing white streaks and defoliation.",
        "precaution": "Use protective gloves. Rotate insecticide classes to prevent resistance."
    },
    "paddy stem maggot": {
        "pesticides": ["Carbofuran 3 G", "Phorate 10 G", "Chlorpyrifos 20 EC"],
        "type": "Carbamate / Organophosphate",
        "crop": "Rice",
        "severity": "High",
        "description": "Maggots bore into rice stems causing dead heart and white ear symptoms.",
        "precaution": "Apply granules at root zone. Avoid contact with skin."
    },
    "asiatic rice borer": {
        "pesticides": ["Cartap Hydrochloride 4 G", "Fipronil 0.3 G", "Chlorantraniliprole 0.4 G"],
        "type": "Nereistoxin analogue / Phenylpyrazole",
        "crop": "Rice",
        "severity": "High",
        "description": "Major rice borer causing dead heart in vegetative stage and white ear at reproductive stage.",
        "precaution": "Apply at early infestation. Drain fields before granule application."
    },
    "yellow rice borer": {
        "pesticides": ["Fipronil 5 SC", "Chlorpyrifos 20 EC", "Triazophos 40 EC"],
        "type": "Phenylpyrazole / Organophosphate",
        "crop": "Rice",
        "severity": "High",
        "description": "The most destructive rice stem borer; larvae bore into stems causing spikelet sterility.",
        "precaution": "Monitor pheromone traps for adult moth population."
    },
    "rice gall midge": {
        "pesticides": ["Carbofuran 3 G", "Phorate 10 G", "Chlorpyrifos 20 EC"],
        "type": "Carbamate / Organophosphate",
        "crop": "Rice",
        "severity": "Medium",
        "description": "Larvae induce gall (silver shoot) formation, destroying the main tiller.",
        "precaution": "Apply at tillering stage. Avoid fish pond contamination."
    },
    "Rice Stemfly": {
        "pesticides": ["Dimethoate 30 EC", "Imidacloprid 17.8 SL", "Thiamethoxam 25 WG"],
        "type": "Organophosphate / Neonicotinoid",
        "crop": "Rice",
        "severity": "Medium",
        "description": "Fly larvae cause dead heart symptoms in early stage rice.",
        "precaution": "Seed treatment with imidacloprid reduces early infestation."
    },
    "brown plant hopper": {
        "pesticides": ["Buprofezin 25 SC", "Imidacloprid 17.8 SL", "Pymetrozine 50 WG"],
        "type": "Insect growth regulator / Neonicotinoid",
        "crop": "Rice",
        "severity": "High",
        "description": "Causes hopperburn by sucking plant sap; vector of grassy stunt and ragged stunt viruses.",
        "precaution": "Avoid excessive nitrogen application. Do not use pyrethroids as they cause resurgence."
    },
    "white backed plant hopper": {
        "pesticides": ["Buprofezin 25 SC", "Ethofenprox 10 EC", "Dinotefuran 20 SG"],
        "type": "Insect growth regulator / Neonicotinoid",
        "crop": "Rice",
        "severity": "High",
        "description": "Sap-sucking pest causing stunting and yellowing; transmits rice stripe and black-streaked dwarf viruses.",
        "precaution": "Apply at base of plant. Maintain field water level during application."
    },
    "small brown plant hopper": {
        "pesticides": ["Imidacloprid 17.8 SL", "Buprofezin 25 SC", "Nitenpyram 10 AS"],
        "type": "Neonicotinoid / IGR",
        "crop": "Rice",
        "severity": "Medium",
        "description": "Vector of rice stripe virus and rice black-streaked dwarf virus.",
        "precaution": "Apply in early morning. Avoid spraying during flowering."
    },
    "rice water weevil": {
        "pesticides": ["Carbofuran 3 G", "Fipronil 0.3 G", "Chlorpyrifos 10 G"],
        "type": "Carbamate / Phenylpyrazole",
        "crop": "Rice",
        "severity": "Medium",
        "description": "Adult and larvae feed on rice roots and leaves, reducing plant vigour.",
        "precaution": "Apply granules to flooded paddies. Harmful to aquatic organisms."
    },
    "rice leafhopper": {
        "pesticides": ["Imidacloprid 17.8 SL", "Thiamethoxam 25 WG", "Acetamiprid 20 SP"],
        "type": "Neonicotinoid",
        "crop": "Rice",
        "severity": "Medium",
        "description": "Transmits tungro virus; causes yellowing and stunting of rice.",
        "precaution": "Rogue out tungro-infected plants. Apply at first sign of hoppers."
    },
    "grain spreader thrips": {
        "pesticides": ["Spinosad 45 SC", "Imidacloprid 17.8 SL", "Dimethoate 30 EC"],
        "type": "Spinosyn / Neonicotinoid",
        "crop": "Rice",
        "severity": "Low",
        "description": "Thrips damage rice spikelets during heading, causing grain discolouration.",
        "precaution": "Apply systemic insecticide at booting stage."
    },
    "rice shell pest": {
        "pesticides": ["Monocrotophos 36 SL", "Chlorpyrifos 20 EC"],
        "type": "Organophosphate",
        "crop": "Rice",
        "severity": "Low",
        "description": "Pest that damages rice grain during development.",
        "precaution": "Monitor field regularly at grain-fill stage."
    },
    "grub": {
        "pesticides": ["Chlorpyrifos 20 EC", "Phorate 10 G", "Imidacloprid 600 FS"],
        "type": "Organophosphate / Neonicotinoid",
        "crop": "General / Turf / Vegetable",
        "severity": "High",
        "description": "White grubs (beetle larvae) feed on roots causing wilting and plant death.",
        "precaution": "Soil drench at planting. Highly toxic — use PPE."
    },
    "mole cricket": {
        "pesticides": ["Chlorpyrifos 10 G", "Carbofuran 3 G", "Fipronil 0.3 G"],
        "type": "Organophosphate / Carbamate",
        "crop": "Turf / Vegetables / Rice",
        "severity": "Medium",
        "description": "Underground pest tunnelling through soil and cutting plant roots.",
        "precaution": "Apply bait formulations at dusk for best results."
    },
    "wireworm": {
        "pesticides": ["Chlorpyrifos 20 EC", "Imidacloprid 600 FS", "Tefluthrin 0.5 G"],
        "type": "Organophosphate / Neonicotinoid",
        "crop": "Corn / Wheat / Potato",
        "severity": "Medium",
        "description": "Larva of click beetles; bores into seeds and roots causing seedling death.",
        "precaution": "Seed treatment is the most effective preventive measure."
    },
    "chinese red solider bug": {
        "pesticides": ["Chlorpyrifos 20 EC", "Lambda-cyhalothrin 5 EC", "Malathion 50 EC"],
        "type": "Organophosphate / Pyrethroid",
        "crop": "Rice / Soybean",
        "severity": "Low",
        "description": "Stink bug that punctures grains causing discolouration and quality loss.",
        "precaution": "Apply at early infestation. Wear mask during application."
    },
    "red spider": {
        "pesticides": ["Abamectin 1.8 EC", "Spiromesifen 22.9 SC", "Hexythiazox 5 EC"],
        "type": "Acaricide / Macrolide",
        "crop": "Vegetables / Fruits / Cotton",
        "severity": "High",
        "description": "Spider mites suck cell contents causing bronzing and leaf drop under hot dry conditions.",
        "precaution": "Rotate miticides. Ensure thorough coverage of leaf undersides."
    },

    # ─── CORN / MAIZE PESTS ──────────────────────────────────────────────────
    "corn borer": {
        "pesticides": ["Chlorantraniliprole 18.5 SC", "Emamectin Benzoate 5 SG", "Spinosad 45 SC"],
        "type": "Diamide / Macrolide / Spinosyn",
        "crop": "Corn",
        "severity": "High",
        "description": "Larvae bore into corn stalks and ears, causing yield losses up to 20%.",
        "precaution": "Apply at whorl stage. Protect honey bees — avoid flowering."
    },
    "black cutworm": {
        "pesticides": ["Lambda-cyhalothrin 5 EC", "Chlorpyrifos 20 EC", "Spinosad 45 SC"],
        "type": "Pyrethroid / Organophosphate",
        "crop": "Corn / Vegetables",
        "severity": "High",
        "description": "Cuts young seedlings at soil level; causes stand loss.",
        "precaution": "Apply at soil surface around plant base. Active at night."
    },
    "large cutworm": {
        "pesticides": ["Chlorpyrifos 20 EC", "Lambda-cyhalothrin 5 EC"],
        "type": "Organophosphate / Pyrethroid",
        "crop": "Corn / Vegetables",
        "severity": "Medium",
        "description": "Larger cutworm species with similar feeding habits to black cutworm.",
        "precaution": "Bait applications effective. Use IPM with pheromone monitoring."
    },
    "tobacco cutworm": {
        "pesticides": ["Emamectin Benzoate 5 SG", "Indoxacarb 14.5 SC", "Chlorantraniliprole 18.5 SC"],
        "type": "Macrolide / Oxadiazine / Diamide",
        "crop": "Tobacco / Corn / Vegetables",
        "severity": "Medium",
        "description": "Polyphagous caterpillar causing severe defoliation.",
        "precaution": "Apply in early instars for best control."
    },
    "beet armyworm": {
        "pesticides": ["Spinosad 45 SC", "Indoxacarb 14.5 SC", "Methomyl 90 SP"],
        "type": "Spinosyn / Oxadiazine / Carbamate",
        "crop": "Beet / Corn / Vegetables",
        "severity": "High",
        "description": "Fast-developing caterpillar; develops resistance rapidly.",
        "precaution": "Rotate insecticide modes of action every generation."
    },
    "alfalfa caterpillar": {
        "pesticides": ["Spinosad 45 SC", "Chlorantraniliprole 18.5 SC", "Bacillus thuringiensis (Bt)"],
        "type": "Biological / Spinosyn / Diamide",
        "crop": "Alfalfa / Forage crops",
        "severity": "Medium",
        "description": "Defoliates alfalfa; population explosions can strip entire fields.",
        "precaution": "Bt is safe for beneficial insects and preferred for organic systems."
    },
    "flax budworm": {
        "pesticides": ["Deltamethrin 2.5 EC", "Cypermethrin 10 EC"],
        "type": "Pyrethroid",
        "crop": "Flax",
        "severity": "Low",
        "description": "Larvae feed on flax buds and capsules, causing yield reduction.",
        "precaution": "Apply at bud formation. Avoid drift to water bodies."
    },
    "alfalfa plant bug": {
        "pesticides": ["Dimethoate 30 EC", "Imidacloprid 17.8 SL", "Pyrethrins + PBO"],
        "type": "Organophosphate / Neonicotinoid",
        "crop": "Alfalfa",
        "severity": "Medium",
        "description": "Piercing-sucking bug causing stippled, wilted terminals in alfalfa.",
        "precaution": "Scout at pre-bloom. Economic threshold is 2 bugs per stem."
    },
    "tarnished plant bug": {
        "pesticides": ["Imidacloprid 17.8 SL", "Acetamiprid 20 SP", "Bifenthrin 10 EC"],
        "type": "Neonicotinoid / Pyrethroid",
        "crop": "Alfalfa / Cotton / Strawberry / Vegetables",
        "severity": "High",
        "description": "Polyphagous; causes cat-facing in fruit crops and bud abortion.",
        "precaution": "Apply at first nymph emergence. Monitor weed hosts."
    },
    "meadow spittlebug": {
        "pesticides": ["Pyrethrin + PBO", "Malathion 50 EC", "Carbaryl 85 WP"],
        "type": "Pyrethrin / Organophosphate / Carbamate",
        "crop": "Alfalfa / Clover / Strawberry",
        "severity": "Low",
        "description": "Nymphs feed inside spittle masses; adults pierce and feed on plant stems.",
        "precaution": "Early cutting of alfalfa disrupts spittlebug development."
    },
    "beet leafhopper": {
        "pesticides": ["Imidacloprid 17.8 SL", "Thiamethoxam 25 WG", "Malathion 50 EC"],
        "type": "Neonicotinoid / Organophosphate",
        "crop": "Beet / Tomato / Bean",
        "severity": "High",
        "description": "Vector of beet curly top virus; causes severe stunting.",
        "precaution": "Apply systemic insecticide at seedling stage."
    },
    "dutch lily thrips": {
        "pesticides": ["Spinosad 45 SC", "Imidacloprid 17.8 SL", "Abamectin 1.8 EC"],
        "type": "Spinosyn / Neonicotinoid / Macrolide",
        "crop": "Lily / Ornamental",
        "severity": "Medium",
        "description": "Damages lily bulbs during storage and causes streaking of petals.",
        "precaution": "Pre-plant bulb treatment. Inspect bulbs before storage."
    },
    "onion thrips": {
        "pesticides": ["Spinosad 45 SC", "Thiamethoxam 25 WG", "Dimethoate 30 EC"],
        "type": "Spinosyn / Neonicotinoid / Organophosphate",
        "crop": "Onion / Garlic",
        "severity": "Medium",
        "description": "Causes silvering of leaves; vector of iris yellow spot virus.",
        "precaution": "Apply when temperature is below 30°C. Thrips hide in leaf base."
    },
    "tobacco thrips": {
        "pesticides": ["Spinosad 45 SC", "Acephate 75 SP", "Imidacloprid 17.8 SL"],
        "type": "Spinosyn / Organophosphate / Neonicotinoid",
        "crop": "Tobacco / Soybean / Cotton",
        "severity": "Medium",
        "description": "Causes bronzing and distortion of leaves; early-season pest.",
        "precaution": "Foliar applications at first flush. Avoid broad-spectrum products."
    },
    "lygus bug": {
        "pesticides": ["Imidacloprid 17.8 SL", "Acetamiprid 20 SP", "Bifenthrin 10 EC"],
        "type": "Neonicotinoid / Pyrethroid",
        "crop": "Alfalfa / Cotton / Strawberry",
        "severity": "Medium",
        "description": "Causes cat-facing in strawberries and tip damage in many crops.",
        "precaution": "Monitor field borders first as lygus moves from maturing crops."
    },

    # ─── COTTON PESTS ────────────────────────────────────────────────────────
    "grape colaspis": {
        "pesticides": ["Chlorpyrifos 20 EC", "Carbaryl 85 WP"],
        "type": "Organophosphate / Carbamate",
        "crop": "Corn / Soybean / Grape",
        "severity": "Low",
        "description": "Adult beetles skeletonise leaves; larvae attack roots.",
        "precaution": "Crop rotation breaks soil larval cycle."
    },
    "colaspis": {
        "pesticides": ["Chlorpyrifos 20 EC", "Lambda-cyhalothrin 5 EC"],
        "type": "Organophosphate / Pyrethroid",
        "crop": "Soybean / Corn",
        "severity": "Low",
        "description": "Similar to grape colaspis; damages soybean and corn seedlings.",
        "precaution": "Seed treatment effective for early-season soil larvae."
    },
    "boll weevil": {
        "pesticides": ["Malathion 50 EC", "Chlorpyrifos 20 EC", "Spinosad 45 SC"],
        "type": "Organophosphate / Spinosyn",
        "crop": "Cotton",
        "severity": "High",
        "description": "Larvae develop inside cotton bolls causing square and boll drop.",
        "precaution": "Use pheromone traps for monitoring. Destroy crop residues."
    },
    "boll worm": {
        "pesticides": ["Chlorantraniliprole 18.5 SC", "Emamectin Benzoate 5 SG", "Indoxacarb 14.5 SC"],
        "type": "Diamide / Macrolide / Oxadiazine",
        "crop": "Cotton / Corn / Tomato",
        "severity": "High",
        "description": "Larvae bore into cotton bolls and corn ears causing severe losses.",
        "precaution": "Bt-cotton reduces need for sprays. Monitor egg counts."
    },
    "linear blotch leafminer": {
        "pesticides": ["Abamectin 1.8 EC", "Spinosad 45 SC", "Cyromazine 75 WP"],
        "type": "Macrolide / Spinosyn / IGR",
        "crop": "Vegetables / Cotton",
        "severity": "Medium",
        "description": "Larvae mine between leaf surfaces creating linear blotch patterns.",
        "precaution": "Introduce parasitic wasps as biological control."
    },
    "vegetable leafminer": {
        "pesticides": ["Abamectin 1.8 EC", "Cyromazine 75 WP", "Spinosad 45 SC"],
        "type": "Macrolide / IGR / Spinosyn",
        "crop": "Tomato / Capsicum / Cucurbits",
        "severity": "Medium",
        "description": "Larvae create serpentine mines in leaves; heavy infestation defoliates plants.",
        "precaution": "Avoid killing parasitoids. Use yellow sticky traps for monitoring."
    },
    "pea leaf miner": {
        "pesticides": ["Abamectin 1.8 EC", "Dimethoate 30 EC"],
        "type": "Macrolide / Organophosphate",
        "crop": "Pea / Bean",
        "severity": "Low",
        "description": "Mines visible on upper leaf surface; reduces photosynthesis.",
        "precaution": "Do not spray during flowering to protect pollinators."
    },
    "podworm": {
        "pesticides": ["Chlorantraniliprole 18.5 SC", "Emamectin Benzoate 5 SG", "Indoxacarb 14.5 SC"],
        "type": "Diamide / Macrolide / Oxadiazine",
        "crop": "Legumes / Vegetables",
        "severity": "High",
        "description": "Larvae bore into pods/fruits causing direct yield loss.",
        "precaution": "Apply at first flower. Harvest pods promptly."
    },
    "lima bean pod borer": {
        "pesticides": ["Emamectin Benzoate 5 SG", "Spinosad 45 SC"],
        "type": "Macrolide / Spinosyn",
        "crop": "Lima Bean",
        "severity": "Medium",
        "description": "Bores into developing lima bean pods.",
        "precaution": "Apply 2–3 sprays at 7-day intervals during podding."
    },
    "bean pod mottle": {
        "pesticides": ["Imidacloprid 17.8 SL", "Thiamethoxam 25 WG"],
        "type": "Neonicotinoid (targets vector)",
        "crop": "Soybean / Bean",
        "severity": "Medium",
        "description": "Virus transmitted by bean leaf beetles; causes mosaic and seed discolouration.",
        "precaution": "Control vector beetle population. Use virus-free seed."
    },
    "tobacco hornworm": {
        "pesticides": ["Spinosad 45 SC", "Chlorantraniliprole 18.5 SC", "Bacillus thuringiensis (Bt)"],
        "type": "Spinosyn / Diamide / Biological",
        "crop": "Tobacco / Tomato",
        "severity": "High",
        "description": "Large caterpillar that defoliates plants rapidly; green with white stripes.",
        "precaution": "Hand-pick where populations are low. Bt is organic-approved."
    },
    "tobacco budworm": {
        "pesticides": ["Emamectin Benzoate 5 SG", "Chlorantraniliprole 18.5 SC", "Indoxacarb 14.5 SC"],
        "type": "Macrolide / Diamide / Oxadiazine",
        "crop": "Tobacco / Cotton / Soybean",
        "severity": "High",
        "description": "Feeds on buds and terminals; resistant to many pyrethroids.",
        "precaution": "Resistance management: rotate modes of action strictly."
    },
    "cotton bollworm": {
        "pesticides": ["Emamectin Benzoate 5 SG", "Chlorantraniliprole 18.5 SC", "Spinosad 45 SC"],
        "type": "Macrolide / Diamide / Spinosyn",
        "crop": "Cotton / Corn / Tomato",
        "severity": "High",
        "description": "One of the most economically important pests worldwide; polyphagous.",
        "precaution": "Pheromone traps to monitor adult population. Use Bt varieties."
    },
    "soybean cyst nematode": {
        "pesticides": ["Fosthiazate 10 G", "Abamectin 1.8 EC", "Fluopyram 40 SC"],
        "type": "Nematicide / Macrolide / SDHI fungicide-nematicide",
        "crop": "Soybean",
        "severity": "High",
        "description": "Microscopic roundworm that attacks soybean roots; causes yellowing and stunting.",
        "precaution": "Crop rotation with non-host crops. Seed treatment most effective."
    },

    # ─── WHEAT PESTS ─────────────────────────────────────────────────────────
    "hessian fly": {
        "pesticides": ["Chlorpyrifos 20 EC", "Dimethoate 30 EC"],
        "type": "Organophosphate",
        "crop": "Wheat / Barley",
        "severity": "High",
        "description": "Larvae stunt wheat plants; adults are small black flies.",
        "precaution": "Fly-free planting dates are most effective. Grow resistant varieties."
    },
    "orange blossom midge": {
        "pesticides": ["Chlorpyrifos 20 EC", "Lambda-cyhalothrin 5 EC"],
        "type": "Organophosphate / Pyrethroid",
        "crop": "Wheat",
        "severity": "Medium",
        "description": "Larvae feed inside developing wheat grain, causing serious losses.",
        "precaution": "Spray at early heading. Monitor adult emergence in spring."
    },
    "wheat jointworm": {
        "pesticides": ["Chlorpyrifos 20 EC", "Dimethoate 30 EC"],
        "type": "Organophosphate",
        "crop": "Wheat",
        "severity": "Medium",
        "description": "Wasp larvae cause stem galling and lodging.",
        "precaution": "Early planting and crop rotation reduce damage."
    },
    "aphid": {
        "pesticides": ["Imidacloprid 17.8 SL", "Thiamethoxam 25 WG", "Pirimicarb 50 WG", "Flonicamid 50 WG"],
        "type": "Neonicotinoid / Selective aphicide",
        "crop": "General (Wheat / Vegetables / Fruits)",
        "severity": "Medium",
        "description": "Sap-sucking insects causing stunting, honeydew deposition and virus transmission.",
        "precaution": "Preserve natural enemies (ladybirds, parasitic wasps). Avoid broad-spectrum sprays."
    },
    "wheat midge": {
        "pesticides": ["Lambda-cyhalothrin 5 EC", "Chlorpyrifos 20 EC"],
        "type": "Pyrethroid / Organophosphate",
        "crop": "Wheat",
        "severity": "Medium",
        "description": "Orange larvae feed inside developing kernels, causing shrivelled grain.",
        "precaution": "Apply at flowering at dusk when adults are active."
    },
    "english grain aphid": {
        "pesticides": ["Pirimicarb 50 WG", "Flonicamid 50 WG", "Imidacloprid 17.8 SL"],
        "type": "Carbamate / Neonicotinoid",
        "crop": "Wheat / Barley / Oat",
        "severity": "Medium",
        "description": "Large green aphid that colonises grain heads; causes yield and quality losses.",
        "precaution": "Treat only when threshold of 5 aphids per ear at GS 69 is exceeded."
    },
    "corn leaf aphid": {
        "pesticides": ["Imidacloprid 17.8 SL", "Thiamethoxam 25 WG", "Malathion 50 EC"],
        "type": "Neonicotinoid / Organophosphate",
        "crop": "Corn",
        "severity": "Low",
        "description": "Blue-green aphids colonising corn tassels; rarely cause economic damage.",
        "precaution": "Natural enemies usually provide adequate control."
    },
    "spotted alfalfa aphid": {
        "pesticides": ["Pirimicarb 50 WG", "Dimethoate 30 EC", "Malathion 50 EC"],
        "type": "Carbamate / Organophosphate",
        "crop": "Alfalfa",
        "severity": "High",
        "description": "Yellow aphid with dark spots; injects toxin causing golden-yellow discolouration.",
        "precaution": "Parasitic wasps and ladybirds are effective biological controls."
    },
    "potato leafhopper": {
        "pesticides": ["Imidacloprid 17.8 SL", "Carbaryl 85 WP", "Malathion 50 EC"],
        "type": "Neonicotinoid / Carbamate / Organophosphate",
        "crop": "Potato / Alfalfa / Bean",
        "severity": "High",
        "description": "Causes hopperburn — marginal leaf scorch and curling; reduces tuber yield.",
        "precaution": "Apply preventively as damage occurs before symptoms appear."
    },
    "grape leafhopper": {
        "pesticides": ["Imidacloprid 17.8 SL", "Acetamiprid 20 SP", "Pyrethrin + PBO"],
        "type": "Neonicotinoid / Pyrethrin",
        "crop": "Grape",
        "severity": "Medium",
        "description": "Stippling and bleaching of grape leaves; affects fruit quality.",
        "precaution": "Preserve parasitic egg wasps. Avoid dusty vineyard roads."
    },
    "citrus mealybug": {
        "pesticides": ["Buprofezin 25 SC", "Spirotetramat 15 OD", "Chlorpyrifos 20 EC"],
        "type": "IGR / Lipid biosynthesis inhibitor / Organophosphate",
        "crop": "Citrus / Grape / Ornamentals",
        "severity": "High",
        "description": "Waxy-covered insects that suck sap; excrete honeydew promoting sooty mould.",
        "precaution": "Release Cryptolaemus beetles for biological control."
    },
    "pine wood nematode": {
        "pesticides": ["Abamectin trunk injection", "Emamectin Benzoate trunk injection"],
        "type": "Macrolide (trunk injection)",
        "crop": "Pine / Conifers",
        "severity": "High",
        "description": "Causes pine wilt disease; spread by pine sawyer beetles.",
        "precaution": "Quarantine infested areas. Trunk injection requires professional application."
    },

    # ─── GENERAL PESTS ───────────────────────────────────────────────────────
    "fall armyworm": {
        "pesticides": ["Emamectin Benzoate 5 SG", "Chlorantraniliprole 18.5 SC", "Spinetoram 12 SC"],
        "type": "Macrolide / Diamide / Spinosyn",
        "crop": "Corn / Sorghum / Rice / Vegetables",
        "severity": "High",
        "description": "Highly invasive polyphagous pest causing devastating crop losses globally.",
        "precaution": "Apply at early whorl stage. Use pheromone traps for adult monitoring."
    },
    "yellow mealworm": {
        "pesticides": ["Deltamethrin 2.5 EC", "Carbaryl 85 WP"],
        "type": "Pyrethroid / Carbamate",
        "crop": "Stored grain / Poultry facilities",
        "severity": "Low",
        "description": "Infests stored grains and poultry litter; larva of darkling beetle.",
        "precaution": "Maintain clean storage. Use physical exclusion methods."
    },
    "pink bollworm": {
        "pesticides": ["Chlorantraniliprole 18.5 SC", "Emamectin Benzoate 5 SG", "Deltamethrin 2.5 EC"],
        "type": "Diamide / Macrolide / Pyrethroid",
        "crop": "Cotton",
        "severity": "High",
        "description": "Larvae feed inside cotton bolls; causes rosette blooms and lint damage.",
        "precaution": "Pheromone mating disruption is highly effective. Destroy crop residues."
    },
    "armyworm": {
        "pesticides": ["Chlorantraniliprole 18.5 SC", "Spinosad 45 SC", "Lambda-cyhalothrin 5 EC"],
        "type": "Diamide / Spinosyn / Pyrethroid",
        "crop": "Corn / Wheat / Rice / Pasture",
        "severity": "High",
        "description": "Caterpillars march in groups stripping leaves and causing complete defoliation.",
        "precaution": "Apply early morning or evening. Treat field borders first to contain migration."
    },
    "greater wax moth": {
        "pesticides": ["Bacillus thuringiensis (Bt) var. galleriae", "Paradichlorobenzene (fumigant)"],
        "type": "Biological / Fumigant",
        "crop": "Beehive / Stored honeycomb",
        "severity": "High",
        "description": "Larvae destroy wax combs in bee hives causing colony collapse.",
        "precaution": "Freeze combs at -18°C for 48 hours to kill all stages."
    },
    "hop vine borer": {
        "pesticides": ["Chlorpyrifos 20 EC", "Deltamethrin 2.5 EC"],
        "type": "Organophosphate / Pyrethroid",
        "crop": "Corn / Hop",
        "severity": "Medium",
        "description": "Larvae bore into corn stalks at base; related to European corn borer.",
        "precaution": "Destroy corn stubble. Tillage exposes overwintering larvae."
    },
    "european corn borer": {
        "pesticides": ["Chlorantraniliprole 18.5 SC", "Emamectin Benzoate 5 SG", "Bt (Bacillus thuringiensis)"],
        "type": "Diamide / Macrolide / Biological",
        "crop": "Corn / Pepper / Potato",
        "severity": "High",
        "description": "Most damaging pest of corn; larvae bore stalks and ears.",
        "precaution": "Pheromone trap monitoring. Bt-corn varieties significantly reduce damage."
    },
    "rough strawberry root weevil": {
        "pesticides": ["Chlorpyrifos 20 EC", "Bifenthrin 10 EC"],
        "type": "Organophosphate / Pyrethroid",
        "crop": "Strawberry / Raspberry / Nursery",
        "severity": "Medium",
        "description": "Adults notch leaves; larvae feed on roots causing sudden plant collapse.",
        "precaution": "Drench soil at transplanting. Apply sticky barriers to plant crowns."
    },
    "rice leaf beetle": {
        "pesticides": ["Chlorpyrifos 20 EC", "Monocrotophos 36 SL", "Malathion 50 EC"],
        "type": "Organophosphate",
        "crop": "Rice",
        "severity": "Medium",
        "description": "Both adults and larvae skeletonise rice leaves.",
        "precaution": "Apply in early morning. Avoid application during tillering."
    },
    "soybean aphid": {
        "pesticides": ["Imidacloprid 17.8 SL", "Thiamethoxam 25 WG", "Flonicamid 50 WG"],
        "type": "Neonicotinoid / Selective aphicide",
        "crop": "Soybean",
        "severity": "Medium",
        "description": "Yellow aphid that rapidly colonises soybean; transmits soybean mosaic virus.",
        "precaution": "Spray when > 250 aphids/plant before R5 growth stage."
    },
    "spider mite": {
        "pesticides": ["Abamectin 1.8 EC", "Bifenazate 24 SC", "Hexythiazox 5 EC", "Spiromesifen 22.9 SC"],
        "type": "Acaricide",
        "crop": "Vegetables / Fruits / Cotton / Ornamentals",
        "severity": "High",
        "description": "Causes stippling and bronzing; thrives in hot dry conditions.",
        "precaution": "Rotate miticide classes. Avoid pyrethroid use which suppresses predatory mites."
    },
    "potato tuber moth": {
        "pesticides": ["Chlorantraniliprole 18.5 SC", "Emamectin Benzoate 5 SG", "Deltamethrin 2.5 EC"],
        "type": "Diamide / Macrolide / Pyrethroid",
        "crop": "Potato",
        "severity": "High",
        "description": "Larvae mine leaves and bore into tubers causing rotting in storage.",
        "precaution": "Maintain tuber coverage with soil. Store at low temperature."
    },
    "potato aphid": {
        "pesticides": ["Imidacloprid 17.8 SL", "Pirimicarb 50 WG", "Flonicamid 50 WG"],
        "type": "Neonicotinoid / Selective aphicide",
        "crop": "Potato",
        "severity": "Medium",
        "description": "Vector of potato virus Y and leafroll virus.",
        "precaution": "Control vectors early to prevent virus spread. Use reflective mulch."
    },
    "harlequin bug": {
        "pesticides": ["Chlorpyrifos 20 EC", "Carbaryl 85 WP", "Malathion 50 EC"],
        "type": "Organophosphate / Carbamate",
        "crop": "Brassica / Vegetables",
        "severity": "Medium",
        "description": "Brightly coloured stink bug that injects toxin causing wilting and plant death.",
        "precaution": "Remove wild brassicas from field borders. Hand-pick egg masses."
    },
    "green stink bug": {
        "pesticides": ["Lambda-cyhalothrin 5 EC", "Chlorpyrifos 20 EC", "Bifenthrin 10 EC"],
        "type": "Pyrethroid / Organophosphate",
        "crop": "Soybean / Corn / Peach",
        "severity": "Medium",
        "description": "Piercing-sucking bug causing cat-facing in fruits and seed shrivelling.",
        "precaution": "Monitor field borders. Apply at nymph stage for best control."
    },
    "kudzu bug": {
        "pesticides": ["Lambda-cyhalothrin 5 EC", "Bifenthrin 10 EC", "Imidacloprid 17.8 SL"],
        "type": "Pyrethroid / Neonicotinoid",
        "crop": "Soybean / Kudzu",
        "severity": "High",
        "description": "Introduced pest that infests soybean stems and pods; causes up to 30% yield loss.",
        "precaution": "Monitor kudzu weed patches as reservoir hosts."
    },
    "squash bug": {
        "pesticides": ["Carbaryl 85 WP", "Permethrin 25 EC", "Imidacloprid 17.8 SL"],
        "type": "Carbamate / Pyrethroid / Neonicotinoid",
        "crop": "Squash / Cucurbit",
        "severity": "High",
        "description": "Injects toxic saliva causing rapid vine wilting; transmits yellow vine disease.",
        "precaution": "Trap boards under plants overnight. Destroy egg masses on leaf undersides."
    },
    "southern green stink bug": {
        "pesticides": ["Lambda-cyhalothrin 5 EC", "Endosulfan 35 EC", "Malathion 50 EC"],
        "type": "Pyrethroid / Organochlorine / Organophosphate",
        "crop": "Soybean / Tomato / Citrus / Mango",
        "severity": "Medium",
        "description": "Causes cloud spotting in tomato and corky patches in citrus.",
        "precaution": "Monitor pheromone traps. Apply in cool morning conditions."
    },
    "whitefly": {
        "pesticides": ["Spirotetramat 15 OD", "Buprofezin 25 SC", "Thiamethoxam 25 WG", "Pyriproxyfen 10 EC"],
        "type": "Lipid biosynthesis inhibitor / IGR / Neonicotinoid",
        "crop": "Tomato / Cotton / Vegetables",
        "severity": "High",
        "description": "Vector of begomoviruses (tomato yellow leaf curl). Honeydew causes sooty mould.",
        "precaution": "Yellow sticky traps for monitoring. Rotate chemical classes. Introduce Encarsia."
    },

    # ─── BRASSICA PESTS ──────────────────────────────────────────────────────
    "diamondback moth": {
        "pesticides": ["Spinosad 45 SC", "Chlorantraniliprole 18.5 SC", "Bacillus thuringiensis (Bt)"],
        "type": "Spinosyn / Diamide / Biological",
        "crop": "Cabbage / Cauliflower / Broccoli",
        "severity": "High",
        "description": "Most resistant pest globally; larvae feed on leaf undersides leaving windowed appearance.",
        "precaution": "Strict rotation of insecticide classes essential. Bt is highly effective."
    },
    "cabbage looper": {
        "pesticides": ["Spinosad 45 SC", "Bacillus thuringiensis (Bt)", "Indoxacarb 14.5 SC"],
        "type": "Spinosyn / Biological / Oxadiazine",
        "crop": "Cabbage / Lettuce / Broccoli",
        "severity": "Medium",
        "description": "Pale green caterpillar that loops as it crawls; chews large holes in leaves.",
        "precaution": "Bt most effective on young instars. Avoid spraying during rain."
    },
    "imported cabbageworm": {
        "pesticides": ["Bacillus thuringiensis (Bt)", "Spinosad 45 SC", "Deltamethrin 2.5 EC"],
        "type": "Biological / Spinosyn / Pyrethroid",
        "crop": "Cabbage / Broccoli / Kale",
        "severity": "Medium",
        "description": "Velvety green caterpillar; feeds on inner leaves and head of cabbage.",
        "precaution": "Row covers prevent adult butterfly egg laying."
    },
    "cabbage aphid": {
        "pesticides": ["Pirimicarb 50 WG", "Imidacloprid 17.8 SL", "Flonicamid 50 WG"],
        "type": "Carbamate / Neonicotinoid / Selective aphicide",
        "crop": "Cabbage / Broccoli / Brussels Sprouts",
        "severity": "Medium",
        "description": "Grey, waxy aphids forming dense colonies; causes distortion of growing point.",
        "precaution": "Selective aphicides preserve parasitic wasps. Do not spray in flowering."
    },
    "cabbage seedpod weevil": {
        "pesticides": ["Chlorpyrifos 20 EC", "Malathion 50 EC", "Lambda-cyhalothrin 5 EC"],
        "type": "Organophosphate / Pyrethroid",
        "crop": "Canola / Rapeseed",
        "severity": "Medium",
        "description": "Adults feed on pollen; larvae develop inside seedpods causing pod shatter.",
        "precaution": "Apply at 20–25% bloom stage."
    },
    "cutworm": {
        "pesticides": ["Chlorpyrifos 20 EC", "Lambda-cyhalothrin 5 EC", "Spinosad 45 SC"],
        "type": "Organophosphate / Pyrethroid / Spinosyn",
        "crop": "Vegetables / Corn / Wheat",
        "severity": "High",
        "description": "Nocturnal caterpillars cutting seedlings at ground level.",
        "precaution": "Bait applications at dusk. Shallow tillage exposes larvae to birds."
    },
    "thrips": {
        "pesticides": ["Spinosad 45 SC", "Imidacloprid 17.8 SL", "Abamectin 1.8 EC"],
        "type": "Spinosyn / Neonicotinoid / Macrolide",
        "crop": "Vegetables / Flowers / Fruits",
        "severity": "Medium",
        "description": "Tiny insects causing silvery streaking; vector of tospoviruses.",
        "precaution": "Blue sticky traps for monitoring. Apply when < 10 thrips/leaf."
    },

    # ─── ALLIUM PESTS ────────────────────────────────────────────────────────
    "leek moth": {
        "pesticides": ["Chlorantraniliprole 18.5 SC", "Spinosad 45 SC", "Bacillus thuringiensis (Bt)"],
        "type": "Diamide / Spinosyn / Biological",
        "crop": "Leek / Onion / Garlic",
        "severity": "Medium",
        "description": "Larvae mine into leek leaves and stem; older larvae bore into shaft.",
        "precaution": "Row covers protect crop. Bt sprays effective on young larvae."
    },
    "onion maggot": {
        "pesticides": ["Chlorpyrifos 20 EC", "Imidacloprid 600 FS (seed treatment)", "Diazinon 50 EC"],
        "type": "Organophosphate / Neonicotinoid",
        "crop": "Onion / Garlic / Leek",
        "severity": "High",
        "description": "Maggots bore into onion bulbs causing rotting.",
        "precaution": "Seed treatment most effective. Crop rotation essential."
    },

    # ─── CORN EARWORM / TOMATO PESTS ─────────────────────────────────────────
    "corn earworm": {
        "pesticides": ["Chlorantraniliprole 18.5 SC", "Emamectin Benzoate 5 SG", "Spinosad 45 SC"],
        "type": "Diamide / Macrolide / Spinosyn",
        "crop": "Corn / Tomato / Cotton / Soybean",
        "severity": "High",
        "description": "Also called tomato fruitworm and cotton bollworm depending on host crop.",
        "precaution": "Apply to corn silks. Monitor with pheromone traps."
    },
    "tomato hornworm": {
        "pesticides": ["Spinosad 45 SC", "Bacillus thuringiensis (Bt)", "Chlorantraniliprole 18.5 SC"],
        "type": "Spinosyn / Biological / Diamide",
        "crop": "Tomato / Pepper / Eggplant",
        "severity": "High",
        "description": "Large green caterpillar with diagonal stripes; defoliates tomato rapidly.",
        "precaution": "Hand-pick. Preserve parasitised caterpillars (white cocoons)."
    },
    "tomato fruitworm": {
        "pesticides": ["Chlorantraniliprole 18.5 SC", "Emamectin Benzoate 5 SG", "Spinosad 45 SC"],
        "type": "Diamide / Macrolide / Spinosyn",
        "crop": "Tomato",
        "severity": "High",
        "description": "Same species as corn earworm; bores into tomato fruit causing decay.",
        "precaution": "Begin sprays when eggs are first detected on leaves."
    },

    # ─── FRUIT PESTS ─────────────────────────────────────────────────────────
    "spotted wing drosophila": {
        "pesticides": ["Spinosad 45 SC", "Malathion 50 EC", "Deltamethrin 2.5 EC"],
        "type": "Spinosyn / Organophosphate / Pyrethroid",
        "crop": "Cherry / Berry / Grape / Stone Fruit",
        "severity": "High",
        "description": "Female infests ripe and ripening soft fruits; larvae cause internal rotting.",
        "precaution": "Short spray intervals (5–7 days) during harvest. Use fine mesh netting."
    },
    "cherry fruit fly": {
        "pesticides": ["Spinosad 45 SC", "Dimethoate 30 EC", "Malathion 50 EC"],
        "type": "Spinosyn / Organophosphate",
        "crop": "Cherry / Sour Cherry",
        "severity": "High",
        "description": "Larvae tunnel through cherry flesh making them unmarketable.",
        "precaution": "Apply at adult emergence using yellow sticky traps as monitoring tool."
    },
    "peach twig borer": {
        "pesticides": ["Chlorantraniliprole 18.5 SC", "Spinosad 45 SC", "Deltamethrin 2.5 EC"],
        "type": "Diamide / Spinosyn / Pyrethroid",
        "crop": "Peach / Nectarine / Almond",
        "severity": "Medium",
        "description": "First-generation larvae bore into new shoots; later generations attack fruit.",
        "precaution": "Apply at dormant stage and at pink bud for shoot protection."
    },
    "peach fruit moth": {
        "pesticides": ["Chlorantraniliprole 18.5 SC", "Emamectin Benzoate 5 SG", "Lambda-cyhalothrin 5 EC"],
        "type": "Diamide / Macrolide / Pyrethroid",
        "crop": "Peach / Apricot / Plum",
        "severity": "High",
        "description": "Larvae bore into peach fruits causing premature drop.",
        "precaution": "Pheromone mating disruption is highly effective."
    },
    "oriental fruit moth": {
        "pesticides": ["Chlorantraniliprole 18.5 SC", "Emamectin Benzoate 5 SG", "Spinosad 45 SC"],
        "type": "Diamide / Macrolide / Spinosyn",
        "crop": "Peach / Apple / Pear",
        "severity": "High",
        "description": "Early-season shoot borer; late-season fruit borer.",
        "precaution": "Mating disruption pheromone dispensers highly effective."
    },
    "codling moth": {
        "pesticides": ["Chlorantraniliprole 18.5 SC", "Emamectin Benzoate 5 SG", "Codling moth granulosis virus"],
        "type": "Diamide / Macrolide / Biological virus",
        "crop": "Apple / Pear / Walnut",
        "severity": "High",
        "description": "Larvae bore into apple core (worm in apple); major orchard pest globally.",
        "precaution": "Begin sprays at petal fall. Pheromone traps for timing. Use CpGV in organic orchards."
    },
    "apple maggot": {
        "pesticides": ["Malathion 50 EC", "Spinosad 45 SC", "Kaolin clay WP"],
        "type": "Organophosphate / Spinosyn / Physical barrier",
        "crop": "Apple / Blueberry",
        "severity": "High",
        "description": "Larvae tunnel through apple flesh creating brown winding trails.",
        "precaution": "Red sphere baited traps. Begin sprays when first adults are caught."
    },
    "apple aphid": {
        "pesticides": ["Pirimicarb 50 WG", "Flonicamid 50 WG", "Imidacloprid 17.8 SL"],
        "type": "Selective aphicide / Neonicotinoid",
        "crop": "Apple",
        "severity": "Medium",
        "description": "Causes leaf curling and shoot stunting; sooty mould on honeydew.",
        "precaution": "Spray at bud burst before colonies become established."
    },
    "woolly apple aphid": {
        "pesticides": ["Spirotetramat 15 OD", "Chlorpyrifos 20 EC", "Imidacloprid 17.8 SL"],
        "type": "Lipid biosynthesis inhibitor / Organophosphate / Neonicotinoid",
        "crop": "Apple",
        "severity": "Medium",
        "description": "White waxy aphid colonising wounds and roots causing gall formation.",
        "precaution": "Introduce Aphelinus mali parasitic wasp for long-term control."
    },
    "plum curculio": {
        "pesticides": ["Phosmet 50 WP", "Carbaryl 85 WP", "Lambda-cyhalothrin 5 EC"],
        "type": "Organophosphate / Carbamate / Pyrethroid",
        "crop": "Apple / Plum / Cherry / Peach",
        "severity": "High",
        "description": "Snout beetle causing characteristic crescent-shaped egg-laying scars on fruit.",
        "precaution": "Apply at petal fall. Kaolin clay repels adults. Jarring trees to collect adults."
    },
    "japanese beetle": {
        "pesticides": ["Imidacloprid 600 FS", "Chlorantraniliprole 18.5 SC", "Carbaryl 85 WP"],
        "type": "Neonicotinoid / Diamide / Carbamate",
        "crop": "Rose / Grape / Apple / Turfgrass",
        "severity": "High",
        "description": "Adults skeletonise leaves and flowers; grubs damage turf roots.",
        "precaution": "Pheromone traps can attract more beetles — place away from crops."
    },
}


def get_pest_info(pest_name: str) -> dict:
    """
    Look up pesticide recommendations for a given pest name.
    Falls back to a generic response if pest not in map.
    """
    # Try exact match first
    if pest_name in PEST_INFO:
        return PEST_INFO[pest_name]

    # Try case-insensitive partial match
    pest_lower = pest_name.lower()
    for key, val in PEST_INFO.items():
        if pest_lower in key.lower() or key.lower() in pest_lower:
            return val

    # Default fallback
    return {
        "pesticides": ["Consult local agricultural extension officer"],
        "type": "Unknown",
        "crop": "Unknown",
        "severity": "Unknown",
        "description": f"No specific recommendation found for '{pest_name}'.",
        "precaution": "Always read the label. Consult a certified agronomist.",
    }
