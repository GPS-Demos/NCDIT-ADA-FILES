# Story: Compute Resource Selection UI
Status: Ready for Review
Epic: 4

## Description
Create the Compute & Software tab with compute resource selection cards.

## Acceptance Criteria
- [x] Compute & Software tab displays "Provision Compute Resources" heading
- [x] Subtitle explains: "Select compute resources and software to analyze this dataset. Resources are provisioned on-demand."
- [x] Four compute option cards are displayed: Standard GPU (V100), High Performance GPU (A100), CPU Only, Distributed Cluster
- [x] Each card shows: icon, title, hardware name, specifications (VRAM/vCPUs/RAM or nodes/total RAM)
- [x] Standard GPU card is selected by default (highlighted border/background)
- [x] Clicking a compute card selects it and deselects others (radio behavior)
- [x] Visual feedback shows selected state: colored border, background tint
- [x] Compute options use card layout with consistent styling and spacing
- [x] Below compute options, "Available Software & Tools" section displays software badges
- [x] Software badges display as styled pills: Python 3.11, PyTorch 2.0, TensorFlow 2.13, NumPy, Pandas, Scikit-learn, Matplotlib, Custom Climate Analysis Toolkit

## Tasks
- [x] Create Compute & Software tab component
- [x] Create compute option cards (4 types)
- [x] Implement radio selection behavior
- [x] Add visual selected state
- [x] Create software badges section
- [x] Style with Tailwind CSS
- [x] Write tests

## Dev Agent Record
### Debug Log
No issues encountered during implementation.

### Completion Notes
Successfully implemented ComputeSoftwareTab component with:
- 4 compute resource cards with icons, titles, hardware names, and specifications
- Radio selection behavior with visual feedback (purple border and background)
- Standard GPU selected by default
- Software badges section with 8 tool badges
- Launch button functionality (Story 4 integrated)
- Loading and success states
- Warning for missing Colab URL
- Comprehensive test coverage (18 test cases)

### File List
- /usr/local/google/home/stonejiang/scitility/frontend/src/components/ComputeSoftwareTab.tsx
- /usr/local/google/home/stonejiang/scitility/frontend/src/components/ComputeSoftwareTab.test.tsx
- /usr/local/google/home/stonejiang/scitility/frontend/src/pages/DataViewerPage.tsx (updated)

### Change Log
- Created ComputeSoftwareTab component with 4 compute resource cards
- Standard GPU (V100): 16GB VRAM, 8 vCPUs, 32GB RAM
- High Performance GPU (A100): 40GB VRAM, 16 vCPUs, 64GB RAM
- CPU Only (Intel Xeon): No GPU, 16 vCPUs, 64GB RAM
- Distributed Cluster: 4 nodes, 160GB total RAM, 4x V100 GPUs
- Implemented radio selection with purple border/background for selected state
- Added selected indicator (checkmark badge) on selected cards
- Created software badges section with 8 tools displayed as blue pills
- Integrated launch button with loading/success states (Story 4)
- Added warning message for datasets without configured notebooks
- Styled with Tailwind CSS following design system
- Integrated into DataViewerPage with state management
- Created comprehensive test suite covering all functionality

## Testing
- Test compute cards render
- Test selection behavior
- Test visual states
- Test software badges
