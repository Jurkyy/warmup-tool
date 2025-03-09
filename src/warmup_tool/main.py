import csv
import pandas as pd

# Define lift-specific tests
LIFT_SPECIFIC_TESTS = {
    "squat": [
        "Ankle Mobility",
        "Hip Flexion",
        "Hip Internal Rotation",
        "Hip External Rotation",
        "Thoracic Extension",
        "Shoulder Internal Rotation",
        "Lat Flexibility",
        "Bracing Ability",
        "Anterior Core Control",
        "Hip Hinge Pattern",
        "Squat Pattern",
    ],
    "bench": [
        "Shoulder External Rotation",
        "Shoulder Internal Rotation",
        "Thoracic Extension",
        "Lat Flexibility",
        "Wrist Mobility",
        "Bracing Ability",
        "Bench Setup",
    ],
    "deadlift": [
        "Hip Flexion",
        "Hamstring Flexibility",
        "Lat Flexibility",
        "Wrist Mobility",
        "Bracing Ability",
        "Anterior Core Control",
        "Hip Hinge Pattern",
        "Deadlift Setup",
    ],
}

FUNDAMENTAL_TESTS = [
    "General Pain Assessment",
    "Muscle Soreness",
    "CNS Fatigue",
]


def load_assessment_data(csv_file):
    """Load the assessment data from CSV file."""
    try:
        df = pd.read_csv(csv_file)
        return df
    except Exception as e:
        print(f"Error loading CSV file: {e}")
        return None


def select_lifts():
    """Allow user to select which lifts they'll be performing."""
    print("\n=== LIFT SELECTION ===\n")
    print("Which lift(s) will you be performing today?")

    lifts = []

    squat = input("Squat? (y/n): ").lower() == "y"
    bench = input("Bench? (y/n): ").lower() == "y"
    deadlift = input("Deadlift? (y/n): ").lower() == "y"

    if squat:
        lifts.append("squat")
    if bench:
        lifts.append("bench")
    if deadlift:
        lifts.append("deadlift")

    return lifts


def get_relevant_tests(lifts):
    """Get relevant tests based on selected lifts."""
    relevant_areas = set(FUNDAMENTAL_TESTS)
    for lift in lifts:
        for test in LIFT_SPECIFIC_TESTS[lift]:
            relevant_areas.add(test)

    return relevant_areas


def run_assessment():
    """Run the powerlifting mobility assessment."""
    # Load assessment data
    assessment_data = load_assessment_data("powerlifting-warmup-assessment.csv")
    if assessment_data is None:
        return

    # Select lifts
    selected_lifts = select_lifts()
    print(f"\nSelected lifts: {', '.join(selected_lifts)}")

    # Get relevant tests
    relevant_areas = get_relevant_tests(selected_lifts)

    print("\n=== POWERLIFTING MOBILITY ASSESSMENT ===\n")
    print(
        f"You'll be assessed on {len(relevant_areas)} relevant tests for your selected lift(s)."
    )
    print(
        "Answer 'y' if you failed the test, 'n' if you passed, or 'skip' to skip a test.\n"
    )

    # Track failed tests
    failed_tests = []

    # Go through each relevant test
    for index, row in assessment_data.iterrows():
        area = row["Area"]

        # Skip irrelevant tests
        if area not in relevant_areas:
            continue

        test = row["Test"]
        description = row["Test_Description"]
        fail_criteria = row["Fail_Criteria"]

        print(f"\n--- {area}: {test} ---")
        print(f"Description: {description}")
        print(f"You fail if: {fail_criteria}")

        while True:
            response = input("\nDid you fail this test? (y/n/skip): ").lower()
            if response in ["y", "n", "skip"]:
                break
            print("Invalid response. Please enter 'y', 'n', or 'skip'.")

        if response == "y":
            failed_tests.append(index)

    # Generate personalized warmup based on failed tests
    generate_warmup_plan(assessment_data, failed_tests, selected_lifts)


def generate_warmup_plan(assessment_data, failed_indices, selected_lifts):
    """Generate a personalized warmup plan based on failed tests."""
    if not failed_indices:
        print("\n=== YOUR WARMUP PLAN ===\n")
        print("Congratulations! You passed all tests. Here's a basic warmup routine:")
        print("1. 5-10 minutes of light cardio (rowing, cycling, or jumping jacks)")

        for lift in selected_lifts:
            print(f"\n2. Standard {lift} progression:")
            print("   - Empty bar: 10-15 reps")
            print("   - 40% of working weight: 8-10 reps")
            print("   - 60% of working weight: 5-8 reps")
            print("   - 75% of working weight: 3-5 reps")
            print("   - 85-90% of working weight: 1-2 reps (optional)")
        return

    print("\n=== YOUR CUSTOMIZED WARMUP PLAN ===\n")
    print("Based on your assessment, here's your personalized warmup routine:")
    print(
        "\n1. Start with 5-10 minutes of light cardio (rowing, cycling, or jumping jacks)"
    )

    print("\n2. Targeted mobility/stability work:")

    # Group failed tests by area
    area_counts = {}
    for idx in failed_indices:
        area = assessment_data.iloc[idx]["Area"]
        if area in area_counts:
            area_counts[area] += 1
        else:
            area_counts[area] = 1

    # Sort failed areas by frequency
    sorted_areas = sorted(area_counts.items(), key=lambda x: x[1], reverse=True)

    # Print top issues
    print(f"\nYour top issues are in these areas (prioritized):")
    for area, count in sorted_areas:
        print(f"- {area}")

    # Show exercises for each failed test (limited to top 3-5 tests for practicality)
    print("\nPerform these corrective exercises:")

    num_exercises = min(5, len(failed_indices))
    for i in range(num_exercises):
        idx = failed_indices[i]
        row = assessment_data.iloc[idx]

        print(f"\n-- {row['Area']}: {row['Test']} --")
        for j in range(1, 4):  # First 3 solutions
            solution = row[f"Solution_{j}"]
            print(f"  {j}. {solution}")

    # Print lift-specific warmup progressions
    for lift in selected_lifts:
        print(f"\n3. Standard {lift} progression:")
        print("   - Empty bar: 10-15 reps")
        print("   - 40% of working weight: 8-10 reps")
        print("   - 60% of working weight: 5-8 reps")
        print("   - 75% of working weight: 3-5 reps")
        print("   - 85-90% of working weight: 1-2 reps (optional)")

    print("\n=== IMPLEMENTATION NOTES ===")
    print(f"For your {', '.join(selected_lifts)} today, consider these adjustments:")

    # Add implementation tips based on failed tests
    lift_specific_tips = {lift: [] for lift in selected_lifts}

    for idx in failed_indices:
        row = assessment_data.iloc[idx]
        if pd.notna(
            row["Solution_4"]
        ):  # Solution_4 typically has implementation advice
            area = row["Area"]
            advice = row["Solution_4"]

            # Determine which lift this advice is most relevant for
            for lift in selected_lifts:
                if area in LIFT_SPECIFIC_TESTS[lift]:
                    lift_specific_tips[lift].append(f"- {area}: {advice}")

    # Print lift-specific implementation tips
    for lift in selected_lifts:
        if lift_specific_tips[lift]:
            print(f"\nFor {lift}:")
            for tip in lift_specific_tips[lift]:
                print(tip)


if __name__ == "__main__":
    run_assessment()
