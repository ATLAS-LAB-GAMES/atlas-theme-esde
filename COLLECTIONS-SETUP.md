# ATLAS Custom Collections Setup

ATLAS Theme for ES-DE v0.1.0 includes dedicated presentation for a set of custom game collections.

Each supported collection is exposed as a normal theme folder at the root of the ATLAS theme so ES-DE can discover and display it as an independently themed collection.

## Included collections

ATLAS currently includes support for:

- Digimon Collection
- EA Sports Collection
- Final Fantasy Collection
- Hogwarts Collection
- Jurassic Park Collection
- Mario Collection
- Middle Earth Collection
- Pokemon Collection
- Sonic Collection
- Yu-Gi-Oh Collection
- Zelda Collection

## ES-DE setting

For the dedicated ATLAS collection views to appear individually, set:

**Main Menu → Game Collection Settings → Group custom collections → Never**

Grouping custom collections can cause ES-DE to display them through a shared collections view instead of their dedicated ATLAS system presentation.

## Creating a supported collection

In ES-DE:

1. Open **Main Menu → Game Collection Settings**.
2. Choose **Create new custom collection from theme**.
3. Select the desired ATLAS collection.
4. Add the games you want included.
5. Confirm that **Group custom collections** is set to **Never**.

## Exact names

Use the collection names exactly as provided by the theme.

For example:

```text
Middle Earth Collection
Final Fantasy Collection
Yu-Gi-Oh Collection
EA Sports Collection
```

Spaces and punctuation are intentional.

The theme relies on matching collection/system identifiers for its metadata and artwork, so changing a collection name can prevent the corresponding ATLAS assets from loading.

## Theme discovery folders

At the root of the repository, each supported collection contains a small `theme.xml` discovery entry.

Example:

```text
Middle Earth Collection/
└── theme.xml
```

The discovery file includes the main ATLAS theme:

```xml
<theme>
  <include>./../theme.xml</include>
</theme>
```

This allows the custom collection to use the normal ATLAS system and gamelist layouts while ES-DE recognizes it as a separately themed collection.

## Collection assets

ATLAS collection presentation follows the same asset and metadata mechanisms used for other systems.

Collection-specific assets may include:

- system/background artwork
- system logos
- metallic title artwork
- ATLAS metadata
- variant-specific artwork

Keep filenames and identifiers consistent with the collection name used by the theme.

## Adding another ATLAS collection

When adding a new collection to the theme:

1. Decide on the final collection name.
2. Create a root discovery folder with that exact name.
3. Add a `theme.xml` containing:

   ```xml
   <theme>
     <include>./../theme.xml</include>
   </theme>
   ```

4. Add the required collection metadata.
5. Add the required logo/title assets.
6. Add artwork for the ATLAS visual variants as required.
7. Create the collection in ES-DE using the matching theme entry.
8. Test both the system view and gamelist view.

## Troubleshooting

### Collection does not appear with its dedicated ATLAS view

Check:

- **Group custom collections** is set to **Never**
- the collection was created **from theme**
- the collection name matches the ATLAS theme entry
- the root collection folder contains `theme.xml`
- filenames and capitalization match the expected collection identifier

### Generic artwork appears

The theme may be falling back because a collection-specific artwork or metadata file is missing or named differently than the collection identifier.

### Collection exists but is grouped with other collections

Change:

**Main Menu → Game Collection Settings → Group custom collections → Never**

and return to the system view.