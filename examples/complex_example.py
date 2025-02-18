from ratesb_python import Analyzer

analyzer = Analyzer("Reaction1: S1->P1; k1 * S1")

# Analyze the model for rate law correctness
analyzer.check_all()

# Display all errors and warnings
print(analyzer.results)

# Check selected errors and warnings
analyzer.checks([1, 2, 1001, 1002])
results = analyzer.results
print(results)

# Display only warnings
warnings = results.get_warnings()
for reaction, messages in warnings.items():
    print(reaction, messages)

# Retrieve messages for a specific reaction
messages = results.get_messages_by_reaction("Reaction1")
print(messages)

# Remove messages for a specific reaction
results.remove_messages_by_reaction("Reaction1")

# Get number of errors and warnings
print("Num Errors: ", results.count_errors())
print("Num Warnings: ", results.count_warnings())