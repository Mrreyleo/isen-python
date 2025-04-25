describe('test filter', () => {
  it('filter', () => {
    cy.visit('/home')
    cy.get('[id^=min_price]').type('99')
    cy.get('[id^=max_price]').type('100')
    cy.contains('Filter').click()
  })
})