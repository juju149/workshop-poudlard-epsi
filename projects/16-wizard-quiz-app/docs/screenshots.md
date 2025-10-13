# 📸 Screenshots & UI Preview

> Note: As this is a code implementation without actual device screenshots, this document provides visual representations and descriptions of the UI screens.

## 🎨 Design System

### Color Palette

```
┌─────────────────────────────────────────┐
│  Background Gradient                    │
│  ┌─────────────────────────────────┐   │
│  │  #1a1a2e  ←→  #16213e  ←→       │   │
│  │  #0f3460                         │   │
│  └─────────────────────────────────┘   │
│                                         │
│  Primary CTA                            │
│  ┌───────────┐                          │
│  │ #e94560   │  (Rouge-rose vif)        │
│  └───────────┘                          │
│                                         │
│  House Colors                           │
│  ┌─┐ #ae0001  Gryffondor (Rouge)       │
│  ┌─┐ #1a472a  Serpentard (Vert)        │
│  ┌─┐ #0e1a40  Serdaigle (Bleu)         │
│  ┌─┐ #ecb939  Poufsouffle (Jaune)      │
│  ┌─┐ #2c3e50  Auror (Gris-bleu)        │
│  ┌─┐ #1a1a1a  Mage Noir (Noir)         │
└─────────────────────────────────────────┘
```

### Typography

```
Titres principaux:    36px, Bold, White
Sous-titres:          24px, Bold, White
Corps de texte:       16px, Regular, White70
Labels/Meta:          14px, Regular, White60
```

---

## 📱 Screen 1: Welcome Screen

### Visual Representation

```
╔═══════════════════════════════════════════════╗
║                                               ║
║                     ⚡                        ║
║                                               ║
║           TU ES UN SORCIER,                   ║
║                HARRY !                        ║
║                                               ║
║   ╔═══════════════════════════════════════╗  ║
║   ║  🧙‍♂️ Découvre ton type de sorcier    ║  ║
║   ║                                       ║  ║
║   ║  Réponds à 20 questions pour         ║  ║
║   ║  découvrir quel type de sorcier      ║  ║
║   ║  sommeille en toi !                  ║  ║
║   ║                                       ║  ║
║   ║  6 types possibles :                 ║  ║
║   ║                                       ║  ║
║   ║  🦁 Gryffondor  •  🐍 Serpentard      ║  ║
║   ║  🦅 Serdaigle   •  🦡 Poufsouffle     ║  ║
║   ║  ⚡ Auror       •  💀 Mage Noir       ║  ║
║   ╚═══════════════════════════════════════╝  ║
║                                               ║
║        ┌───────────────────────────┐          ║
║        │  COMMENCER LE QUIZ  ▶    │          ║
║        └───────────────────────────┘          ║
║                                               ║
║              ⏱️ Environ 5 minutes             ║
║                                               ║
╚═══════════════════════════════════════════════╝
```

### UI Elements

1. **Lightning Bolt (⚡)** - 80px emoji, centered
2. **Title** - Two-line title with emphasis on "HARRY !"
3. **Info Card** - Semi-transparent white card (opacity 0.1)
4. **Type List** - Grid of 6 wizard types with emojis
5. **CTA Button** - Large red-pink button with arrow icon
6. **Time Indicator** - Subtle text at bottom

### Interactions

- Tap "COMMENCER LE QUIZ" → Navigate to Quiz Screen
- Smooth fade transition (300ms)

---

## 📱 Screen 2: Quiz Screen

### Visual Representation

```
╔═══════════════════════════════════════════════╗
║  Question 7/20                           35%  ║
║  [▓▓▓▓▓▓▓░░░░░░░░░░░░░░░░░░░]                ║
║                                               ║
║   ╔═══════════════════════════════════════╗  ║
║   ║                                       ║  ║
║   ║   Quelle est votre qualité           ║  ║
║   ║        principale ?                   ║  ║
║   ║                                       ║  ║
║   ╚═══════════════════════════════════════╝  ║
║                                               ║
║        ┌───────────────────────┐              ║
║        │       Courage         │              ║
║        └───────────────────────┘              ║
║                                               ║
║        ┌───────────────────────┐              ║
║        │      Ambition         │              ║
║        └───────────────────────┘              ║
║                                               ║
║        ┌───────────────────────┐              ║
║        │    Intelligence       │              ║
║        └───────────────────────┘              ║
║                                               ║
║        ┌───────────────────────┐              ║
║        │       Loyauté         │              ║
║        └───────────────────────┘              ║
║                                               ║
╚═══════════════════════════════════════════════╝
```

### UI Elements

1. **Progress Header**
   - Question counter (left): "Question X/20"
   - Percentage (right): "35%"
   - Progress bar: Red gradient, 8px height

2. **Question Card**
   - Semi-transparent card
   - Large centered text (24px)
   - Ample padding

3. **Answer Buttons**
   - 4 buttons stacked vertically
   - Semi-transparent background (opacity 0.15)
   - White border (opacity 0.3, 2px)
   - 16px border radius
   - Hover effect: slight brightness increase

### Interactions

- Tap any answer → Fade out (150ms) → Score update → Fade in next question (150ms)
- Last question → Navigate to Result Screen with celebration animation

### Animation Flow

```
Question N
    ↓ (tap answer)
Fade out (150ms)
    ↓
Update scores
    ↓
Load Question N+1
    ↓
Fade in (150ms)
```

---

## 📱 Screen 3: Result Screen

### Visual Representation (Gryffondor Example)

```
╔═══════════════════════════════════════════════╗
║                                               ║
║                ✨ 🎉 ✨                       ║
║                                               ║
║               Tu es un...                     ║
║                                               ║
║                   🦁                          ║
║                                               ║
║         Sorcier de Gryffondor                 ║
║                                               ║
║             🔴 Rouge et Or                    ║
║                                               ║
║   ╔═══════════════════════════════════════╗  ║
║   ║  📜 Description                       ║  ║
║   ║                                       ║  ║
║   ║  Courageux, audacieux et             ║  ║
║   ║  chevaleresque                        ║  ║
║   ║                                       ║  ║
║   ║  Vous êtes brave, déterminé et       ║  ║
║   ║  prêt à défendre vos amis. Vous      ║  ║
║   ║  n'hésitez pas à prendre des         ║  ║
║   ║  risques pour faire ce qui est       ║  ║
║   ║  juste.                               ║  ║
║   ╚═══════════════════════════════════════╝  ║
║                                               ║
║   ╔═══════════════════════════════════════╗  ║
║   ║  ⭐ Sorciers célèbres                 ║  ║
║   ║                                       ║  ║
║   ║  Harry Potter, Hermione Granger,     ║  ║
║   ║  Albus Dumbledore                     ║  ║
║   ╚═══════════════════════════════════════╝  ║
║                                               ║
║   ╔═══════════════════════════════════════╗  ║
║   ║  📊 Détail des scores                 ║  ║
║   ║                                       ║  ║
║   ║  🦁 Gryffondor    42 pts (35%)       ║  ║
║   ║  [▓▓▓▓▓▓▓░░░░░░░░░░░]                ║  ║
║   ║                                       ║  ║
║   ║  🐍 Serpentard    28 pts (23%)       ║  ║
║   ║  [▓▓▓▓░░░░░░░░░░░░░]                 ║  ║
║   ║                                       ║  ║
║   ║  🦅 Serdaigle     25 pts (21%)       ║  ║
║   ║  [▓▓▓░░░░░░░░░░░░░]                  ║  ║
║   ║                                       ║  ║
║   ║  🦡 Poufsouffle   18 pts (15%)       ║  ║
║   ║  [▓▓░░░░░░░░░░░░░░]                  ║  ║
║   ║                                       ║  ║
║   ║  ⚡ Auror          5 pts  (4%)       ║  ║
║   ║  [░░░░░░░░░░░░░░░░░]                 ║  ║
║   ║                                       ║  ║
║   ║  💀 Mage Noir      2 pts  (2%)       ║  ║
║   ║  [░░░░░░░░░░░░░░░░░]                 ║  ║
║   ╚═══════════════════════════════════════╝  ║
║                                               ║
║        ┌───────────────────────┐              ║
║        │  🔄 RECOMMENCER       │              ║
║        └───────────────────────┘              ║
║                                               ║
╚═══════════════════════════════════════════════╝
```

### UI Elements

1. **Celebration**
   - Confetti emojis (✨🎉✨)
   - "Tu es un..." intro text

2. **Result Display**
   - Large wizard emoji (100px)
   - Wizard type name (32px, bold)
   - House colors with emoji

3. **Description Card**
   - Main characteristic (bold)
   - Detailed personality description

4. **Famous Wizards Card**
   - List of 3 famous wizards
   - Related to the type

5. **Score Breakdown**
   - All 6 types listed
   - Points and percentages
   - Visual progress bars (color-coded)
   - Winning type highlighted

6. **Restart Button**
   - Red-pink CTA button
   - Refresh icon

### Dynamic Theming

The background gradient adapts to the winning wizard type:

```
Gryffondor:  #ae0001 → #1a1a2e (Red to dark)
Serpentard:  #1a472a → #1a1a2e (Green to dark)
Serdaigle:   #0e1a40 → #1a1a2e (Blue to dark)
Poufsouffle: #ecb939 → #1a1a2e (Yellow to dark)
Auror:       #2c3e50 → #1a1a2e (Grey to dark)
Mage Noir:   #1a1a1a → #1a1a2e (Black to dark)
```

### Interactions

- Tap "RECOMMENCER" → Reset state → Navigate to Welcome Screen
- Smooth fade transition
- (Future) Share button → Share to social media

---

## 🎬 Animations

### 1. Welcome → Quiz Transition

```
[Welcome Screen]
      ↓
  Fade out (200ms)
      ↓
  Load Quiz
      ↓
  Slide in from right (300ms)
```

### 2. Question Transitions

```
[Current Question visible]
      ↓
  User taps answer
      ↓
  Fade out (150ms)
      ↓
  Update internal scores
      ↓
  Load next question
      ↓
  Fade in (150ms)
```

### 3. Quiz → Result Transition

```
[Last Question answered]
      ↓
  Fade out (200ms)
      ↓
  Calculate final scores
      ↓
  Determine wizard type
      ↓
  Fade in + Scale (500ms)
      ↓
  Display result
      ↓
  Confetti animation (text pulse)
```

### 4. Progress Bar Animation

```
Linear interpolation
From: current percentage
To: next percentage
Duration: 300ms
Easing: ease-in-out
```

---

## 📐 Responsive Design

### Mobile Portrait (Primary)

```
Width:  360-414px (standard phones)
Height: 640-896px
Orientation: Portrait
Elements: Stacked vertically
```

### Mobile Landscape

```
Width:  640-896px
Height: 360-414px
Orientation: Landscape
Elements: Adjusted padding
Note: Less optimal, but functional
```

### Tablet

```
Width:  768-1024px
Height: 1024-1366px
Elements: Centered with max-width
Buttons: Larger touch targets
```

---

## 🎨 Component Library

### Button Styles

```dart
// Primary CTA
ElevatedButton(
  backgroundColor: #e94560,
  foregroundColor: white,
  padding: 48px horizontal, 20px vertical,
  borderRadius: 30px,
  elevation: 8,
)

// Answer Button
ElevatedButton(
  backgroundColor: white.withOpacity(0.15),
  foregroundColor: white,
  padding: 20px all,
  borderRadius: 16px,
  border: white.withOpacity(0.3), 2px,
)
```

### Card Styles

```dart
Card(
  color: white.withOpacity(0.1),
  elevation: 8,
  borderRadius: 16px,
  padding: 24px,
)
```

---

## 🖼️ UI States

### Loading State (Initial)

```
╔══════════════════════╗
║                      ║
║        ⚡            ║
║                      ║
║   TU ES UN SORCIER,  ║
║       HARRY !        ║
║                      ║
╚══════════════════════╝
```

### Active Quiz State

- Question visible
- Answers tappable
- Progress updating
- Smooth transitions

### Result State

- Final scores calculated
- Winner determined
- Detailed breakdown shown
- Restart available

### Error State (not implemented)

Future consideration for network errors or crashes.

---

## 🔍 Accessibility Features

### Current Implementation

✅ **High Contrast** - White text on dark background  
✅ **Large Touch Targets** - 48dp minimum  
✅ **Clear Typography** - 16px+ for readability  
✅ **Visual Feedback** - Button states visible  

### Future Enhancements

🔲 Screen reader support (Semantics widgets)  
🔲 Font scaling support  
🔲 Reduced motion option  
🔲 Color blind friendly mode  

---

## 📱 Platform-Specific Adaptations

### Android

- Material Design 3 components
- System navigation gestures
- Adaptive icons
- Splash screen

### iOS

- Cupertino fallbacks where appropriate
- iOS navigation patterns respected
- SF Symbols compatibility
- Launch screen

---

## 🎯 Visual Hierarchy

```
Priority Level 1 (Most Important):
- Wizard type result (100px emoji)
- CTA buttons (Start Quiz, Recommencer)

Priority Level 2:
- Question text (24px)
- Answer buttons
- Progress bar

Priority Level 3:
- Descriptions
- Scores breakdown
- Famous wizards list

Priority Level 4:
- Meta information (time estimate)
- Question counter
```

---

## 📊 Screen Comparison

| Element | Welcome | Quiz | Result |
|---------|---------|------|--------|
| Header | Title | Progress | Celebration |
| Primary | CTA Button | Question | Wizard Type |
| Secondary | Info Card | Answers | Description |
| Tertiary | Time Estimate | - | Score Details |
| Action | Start | Answer | Restart |

---

> 🎨 *"Le design est la magie qui rend l'invisible visible, et le complexe simple."*

**Note:** For actual screenshots, run the app on an emulator or device and capture screens using device screenshot tools.
